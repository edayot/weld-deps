from beet import Context, configurable, DataPack, ResourcePack
from pprint import pprint
from pydantic import BaseModel
from typing_extensions import TypedDict, NotRequired, Union, Optional, Generator
from enum import Enum
import json
import requests
import pathlib
from smithed import weld
import semver

class PackNotFoundError(Exception):
    pass

class PackVersionNotFoundError(Exception):
    pass

class Source(str, Enum):
    integrated = "integrated"
    smithed = "smithed"
    download = "download"
    modrinth = "modrinth"

class Downloads(TypedDict):
    resourcepack: NotRequired[str]
    datapack: NotRequired[str]

class ResolvedDep(BaseModel):
    id: str
    name: str
    downloads: Downloads

    def download(self, ctx: Context) -> tuple[pathlib.Path | None, pathlib.Path | None]:
        cache = ctx.cache["weld_deps"]
        rp, dp = None, None
        if url := self.downloads.get("resourcepack"):
            rp = cache.download(url)
        if url := self.downloads.get("datapack"):
            dp = cache.download(url)
        return rp, dp

class SmartVersionOpts(BaseModel):
    version: str
    source: Optional[Source] = None
    download: Optional[Downloads] = None

class SmartDepOpts(SmartVersionOpts):
    id: str


VersionOpts = Union[SmartVersionOpts, str]
DepSource = Union[dict[str, VersionOpts], list[SmartDepOpts]]

class DepsConfig(BaseModel):
    enabled: bool = True
    default_source: Source = Source.smithed
    deps: DepSource = {}

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

    def resolve(self, ctx: Context, resolved_deps : list[ResolvedDep], id: str, dep: SmartVersionOpts):
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
        else:
            raise ValueError(f"Unknown source {dep.source}")
    
    def resolve_download(self, ctx: Context, resolved_deps : list[ResolvedDep], id: str, dep: SmartVersionOpts):
        if not dep.download:
            raise ValueError(f"Download source {dep.source} requires a download url")
        resolved_deps.append(ResolvedDep(
            id=id,
            name=dep.version,
            downloads=dep.download
        ))
        return

    def resolve_smithed(self, ctx: Context, resolved_deps : list[ResolvedDep], id: str, dep: SmartVersionOpts):
        url = f"https://api.smithed.dev/v2/packs/{id}"
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
            raise PackVersionNotFoundError(f"Version {dep.version} of pack {id} not found")
        version = versions[0]
        resolved_deps.append(ResolvedDep(
            id=data["id"],
            name=version["name"],
            downloads=Downloads(**version["downloads"])
        ))
        for self_deps in version.get("dependencies", []):
            new_dep = SmartVersionOpts(
                version=self_deps["version"],
                source=Source.smithed
            )
            self.resolve(ctx, resolved_deps, self_deps["id"], new_dep)

    def resolve_modrinth(self, ctx: Context, resolved_deps : list[ResolvedDep], id: str, dep: SmartVersionOpts):
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
            raise PackVersionNotFoundError(f"Version {dep.version} of pack {id} not found")
        version = versions[0]
        is_datapack = "datapack" in version["loaders"]
        is_resourcepack = "minecraft" in version["loaders"]
        if is_datapack and is_resourcepack:
            raise ValueError(f"Pack {id} is both a datapack and a resourcepack")
        downloads : Downloads = {}
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
        resolved_deps.append(ResolvedDep(
            id=id,
            name=dep.version,
            downloads=downloads
        ))
        for self_deps in version.get("dependencies", []):
            if not self_deps["dependency_type"] == "required":
                continue
            self_url = f"https://api.modrinth.com/v2/project/{self_deps['project_id']}/version"
            self_url_2 = f"https://api.modrinth.com/v2/project/{self_deps['project_id']}"
            try:
                self_path = cache.download(self_url)
                self_path_2 = cache.download(self_url_2)
            except requests.HTTPError as e:
                raise PackNotFoundError(f"Pack {id} not found") from e
            self_data = json.loads(self_path.read_text())
            self_data_2 = json.loads(self_path_2.read_text())
            self_versions = filter(lambda x: x["id"] == self_deps["version_id"], self_data)
            self_versions = list(self_versions)
            if len(self_versions) != 1:
                raise PackVersionNotFoundError(f"Version {self_deps['version_id']} of pack {self_deps['project_id']} not found")
            self_version = self_versions[0]
            new_dep = SmartVersionOpts(
                version=self_version["version_number"],
                source=Source.modrinth
            )
            self.resolve(ctx, resolved_deps, self_data_2["slug"], new_dep)


def remove_duplicates(resolved_deps : list[ResolvedDep]):
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
    


@configurable("weld_deps", validator=DepsConfig)
def beet_default(ctx: Context, opts: DepsConfig):
    if not opts.enabled:
        return
    weld.toolchain.main.weld(ctx)
    
    resolved_deps : list[ResolvedDep] = []
    for id, dep in opts.deps_dict():
        opts.resolve(ctx, resolved_deps, id, dep)
    resolved_deps = remove_duplicates(resolved_deps)
    resolved_deps.sort(key=lambda x: x.name)
    for dep in resolved_deps:
        rp, dp = dep.download(ctx)
        if rp:
            ctx.require(weld.toolchain.main.subproject_config(weld.toolchain.main.PackType.ASSETS, str(rp)))       
        if dp:
            ctx.require(weld.toolchain.main.subproject_config(weld.toolchain.main.PackType.DATA, str(dp)))         

