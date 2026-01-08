from beet import Context, configurable, DataPack, ResourcePack
from pprint import pprint
from pydantic import AliasChoices, BaseModel, Field
from typing_extensions import TypedDict, NotRequired, Union, Optional, Generator
from enum import Enum
import json
import requests
import pathlib
import semver
import logging

log = logging.getLogger("weld_deps")


class WeldDepsError(Exception):
    pass


class PackNotFoundError(WeldDepsError):
    pass


class PackVersionNotFoundError(WeldDepsError):
    pass


class Source(str, Enum):
    integrated = "integrated"
    smithed = "smithed"
    download = "download"
    modrinth = "modrinth"
    local = "local"


class Downloads(TypedDict):
    resourcepack: NotRequired[str]
    datapack: NotRequired[str]


class ResolvedDep(BaseModel):
    id: str
    name: str
    downloads: Downloads
    source: Source

    def download(
        self, ctx: Context
    ) -> tuple[pathlib.Path | str | None, pathlib.Path | str | None]:
        if self.source == Source.local:
            return self.downloads.get("resourcepack"), self.downloads.get("datapack")
        cache = ctx.cache["weld_deps"]
        rp, dp = None, None
        if url := self.downloads.get("resourcepack"):
            rp = cache.download(url)
        if url := self.downloads.get("datapack"):
            dp = cache.download(url)
        return rp, dp


class SmartVersionOpts(BaseModel):
    version: str = Field(validation_alias=AliasChoices("version", "version_"))
    source: Optional[Source] = None
    download: Optional[Downloads] = None
    local: Optional[Downloads] = None


class SmartDepOpts(SmartVersionOpts):
    id: str


VersionOpts = Union[SmartVersionOpts, str]
DepSource = Union[dict[str, VersionOpts], list[SmartDepOpts]]


class DepsConfig(BaseModel):
    enabled: bool = True
    default_source: Source = Source.smithed
    merge_after: Optional[bool] = None
    deps: DepSource = {}
    plugin_deps: Optional[list[SmartDepOpts]] = None
    merge_with_weld: bool = True

    def deps_dict(self) -> Generator[tuple[str, SmartVersionOpts], None, None]:
        if isinstance(self.deps, dict):
            for k, v in self.deps.items():
                if isinstance(v, str):
                    yield k, SmartVersionOpts(version=v, source=self.default_source)
                elif isinstance(v, SmartVersionOpts):
                    yield k, v
                else:
                    raise ValueError(f"Invalid dependency {k}: {v}")
        elif isinstance(self.deps, list):
            for v in self.deps:
                if isinstance(v, SmartDepOpts):
                    yield v.id, v
                else:
                    raise ValueError(f"Invalid dependency {v}")
        else:
            raise ValueError(f"Invalid deps {self.deps}")

    def plugin_deps_dict(self) -> Generator[tuple[str, SmartVersionOpts], None, None]:
        if self.plugin_deps is None:
            return
        for v in self.plugin_deps:
            if isinstance(v, SmartDepOpts):
                yield v.id, v
            else:
                raise ValueError(f"Invalid dependency {v}")

    def resolve(
        self,
        ctx: Context,
        resolved_deps: list[ResolvedDep],
        id: str,
        dep: SmartVersionOpts,
    ):
        if dep.source is None:
            dep.source = self.default_source
        if dep.source == Source.integrated:
            return
        elif dep.source == Source.download:
            return self.resolve_download(ctx, resolved_deps, id, dep)
        elif dep.source == Source.smithed:
            return self.resolve_smithed(ctx, resolved_deps, id, dep)
        elif dep.source == Source.modrinth:
            return self.resolve_modrinth(ctx, resolved_deps, id, dep)
        elif dep.source == Source.local:
            assert dep.local, "Local source requires a local path parameter"
            return resolved_deps.append(
                ResolvedDep(
                    id=id, name=dep.version, downloads=dep.local, source=Source.local
                )
            )
        else:
            raise ValueError(f"Unknown source {dep.source}")

    def resolve_download(
        self,
        ctx: Context,
        resolved_deps: list[ResolvedDep],
        id: str,
        dep: SmartVersionOpts,
    ):
        if not dep.download:
            raise ValueError(f"Download source {dep.source} requires a download url")
        resolved_deps.append(
            ResolvedDep(
                id=id, name=dep.version, downloads=dep.download, source=Source.download
            )
        )
        return

    def resolve_smithed(
        self,
        ctx: Context,
        resolved_deps: list[ResolvedDep],
        id: str,
        dep: SmartVersionOpts,
    ):
        id_url = id.split(":")[-1] if ":" in id else id
        url = f"https://api.smithed.dev/v2/packs/{id_url}"
        cache = ctx.cache["weld_deps"]
        path = cache.get_path(url)
        if not path.exists():
            response = requests.get(url)
            try:
                response.raise_for_status()
            except requests.HTTPError as e:
                raise PackNotFoundError(f"Pack {id} not found") from e
            path.write_text(response.text)
        data = json.loads(path.read_text())

        versions = filter(lambda x: x["name"] == dep.version, data["versions"])
        versions = list(versions)
        if len(versions) == 0:
            if dep.version == "latest" and len(data["versions"]) > 0:
                version = max(
                    data["versions"],
                    key=lambda x: semver.VersionInfo.parse(x["name"]),
                )
            else:
                raise PackVersionNotFoundError(
                    f"Version {dep.version} of pack {id} not found"
                )
        else:
            version = versions[0]
        resolved_deps.append(
            ResolvedDep(
                id=data["id"],
                name=version["name"],
                downloads=Downloads(**version["downloads"]),
                source=Source.smithed,
            )
        )
        for self_deps in version.get("dependencies", []):
            new_dep = SmartVersionOpts(
                version=self_deps["version"], source=Source.smithed
            )
            self.resolve(ctx, resolved_deps, self_deps["id"], new_dep)

    def resolve_modrinth(
        self,
        ctx: Context,
        resolved_deps: list[ResolvedDep],
        id: str,
        dep: SmartVersionOpts,
    ):
        url = f"https://api.modrinth.com/v2/project/{id}/version"
        cache = ctx.cache["weld_deps"]
        try:
            path = cache.download(url)
        except requests.HTTPError as e:
            raise PackNotFoundError(f"Pack {id} not found") from e
        data = json.loads(path.read_text())
        versions = filter(lambda x: x["version_number"] == dep.version, data)
        versions = list(versions)
        if len(versions) != 1:
            if dep.version == "latest" and len(data) > 0:
                version = max(
                    data, key=lambda x: semver.VersionInfo.parse(x["version_number"])
                )
            else:
                raise PackVersionNotFoundError(
                    f"Version {dep.version} of pack {id} not found"
                )
        else:
            version = versions[0]
        is_datapack = "datapack" in version["loaders"]
        is_resourcepack = "minecraft" in version["loaders"]
        if is_datapack and is_resourcepack:
            raise ValueError(f"Pack {id} is both a datapack and a resourcepack")
        downloads: Downloads = {}
        files = version["files"]
        primary_files = [x for x in files if x["primary"]]
        not_primary_files = [x for x in files if not x["primary"]]
        if is_datapack:
            assert len(primary_files) == 1
            assert len(not_primary_files) == 0 or len(not_primary_files) == 1
            downloads["datapack"] = primary_files[0]["url"]
            if len(not_primary_files) == 1:
                downloads["resourcepack"] = not_primary_files[0]["url"]
        if is_resourcepack:
            assert len(primary_files) == 1
            assert len(not_primary_files) == 0
            downloads["resourcepack"] = primary_files[0]["url"]
        resolved_deps.append(
            ResolvedDep(
                id=id, name=dep.version, downloads=downloads, source=Source.modrinth
            )
        )
        for self_deps in version.get("dependencies", []):
            if not self_deps["dependency_type"] == "required":
                continue
            self_url = (
                f"https://api.modrinth.com/v2/project/{self_deps['project_id']}/version"
            )
            self_url_2 = (
                f"https://api.modrinth.com/v2/project/{self_deps['project_id']}"
            )
            try:
                self_path = cache.download(self_url)
                self_path_2 = cache.download(self_url_2)
            except requests.HTTPError as e:
                raise PackNotFoundError(f"Pack {id} not found") from e
            self_data = json.loads(self_path.read_text())
            self_data_2 = json.loads(self_path_2.read_text())
            self_versions = filter(
                lambda x: x["id"] == self_deps["version_id"], self_data
            )
            self_versions = list(self_versions)
            if len(self_versions) != 1:
                raise PackVersionNotFoundError(
                    f"Version {self_deps['version_id']} of pack {self_deps['project_id']} not found"
                )
            self_version = self_versions[0]
            new_dep = SmartVersionOpts(
                version=self_version["version_number"], source=Source.modrinth
            )
            self.resolve(ctx, resolved_deps, self_data_2["slug"], new_dep)


def remove_duplicates(resolved_deps: list[ResolvedDep]):
    new_deps = {}
    keep_two = []
    for dep in resolved_deps:
        if dep.id not in new_deps:
            new_deps[dep.id] = dep
        else:
            try:
                version_a = new_deps[dep.id].name
                version_b = dep.name
                version_a = semver.VersionInfo.parse(version_a)
                version_b = semver.VersionInfo.parse(version_b)
                if version_a < version_b:
                    new_deps[dep.id] = dep
            except ValueError as e:
                keep_two.append(dep)
    return list(new_deps.values()) + keep_two


def beet_default(ctx: Context, max_retries: int = 1):
    try:
        ctx.require(internal_plugin)
    except WeldDepsError as e:
        if max_retries > 0:
            ctx.cache["weld_deps"].clear()
            ctx.require(lambda c: beet_default(c, max_retries - 1))
        else:
            raise e


@configurable("weld_deps", validator=DepsConfig)
def internal_plugin(ctx: Context, opts: DepsConfig) -> Generator[None, None, None]:
    if not opts.enabled:
        return
    if opts.merge_with_weld:
        try:
            from smithed import weld
        except ImportError as e:
            raise ImportError(
                "smithed-python is required for merge_with_weld option"
            ) from e
        weld.toolchain.main.weld(ctx)
    ctx.cache["weld_deps"].timeout(days=30)
    if opts.merge_after:
        yield

    resolved_deps: list[ResolvedDep] = []
    for id, dep in opts.deps_dict():
        opts.resolve(ctx, resolved_deps, id, dep)
    plugin_deps: list[ResolvedDep] = []
    for id, dep in opts.plugin_deps_dict():
        opts.resolve(ctx, plugin_deps, id, dep)
    resolved_deps = remove_duplicates(resolved_deps)
    # we add plugin deps only if they are not already present
    for dep in plugin_deps:
        if all(existing_dep.id != dep.id for existing_dep in resolved_deps):
            resolved_deps.append(dep)
            log.info(f"A plugin has added the dependency {dep.id} version {dep.name}")
    resolved_deps.sort(key=lambda x: x.name)

    # actual pack downloading + merging
    for dep in resolved_deps:
        rp, dp = dep.download(ctx)
        if rp:
            if opts.merge_with_weld:
                from smithed import weld

                ctx.require(
                    weld.toolchain.main.subproject_config(
                        weld.toolchain.main.PackType.ASSETS, str(rp)
                    )
                )
            else:
                ctx.assets.merge(ResourcePack(name=f"weld_dep_{dep.id}", path=str(rp)))
        if dp:
            if opts.merge_with_weld:
                from smithed import weld

                ctx.require(
                    weld.toolchain.main.subproject_config(
                        weld.toolchain.main.PackType.DATA, str(dp)
                    )
                )
            else:
                ctx.data.merge(DataPack(name=f"weld_dep_{dep.id}", path=str(dp)))
