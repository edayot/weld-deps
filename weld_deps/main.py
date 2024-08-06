from beet import Context, configurable, DataPack, ResourcePack
from pprint import pprint
from pydantic import BaseModel
from typing_extensions import TypedDict, NotRequired, Union, Optional
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

class Downloads(TypedDict):
    resourcepack: NotRequired[str]
    datapack: NotRequired[str]

class WeldDep(BaseModel):
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

class WeldDepOptions(BaseModel):
    version: str
    source: Source = Source.smithed
    force_download_rp: Optional[str] = None
    force_download_dp: Optional[str] = None


class WeldDepsConfig(BaseModel):
    enabled: bool = True
    deps: dict[str, WeldDepOptions] = {}

    def resolve_integrated(self, ctx: Context, resolved_deps : list[WeldDep], id: str, dep: WeldDepOptions):
        return
    def resolve_download(self, ctx: Context, resolved_deps : list[WeldDep], id: str, dep: WeldDepOptions):
        dl: Downloads = {}
        if dep.force_download_rp:
            dl["resourcepack"] = dep.force_download_rp
        if dep.force_download_dp:
            dl["datapack"] = dep.force_download_dp
        resolved_deps.append(WeldDep(
            id=id,
            name=dep.version,
            downloads=dl
        ))
        return

    
    def resolve(self, ctx: Context, resolved_deps : list[WeldDep], id: str, dep: WeldDepOptions):
        if dep.source == Source.integrated:
            return self.resolve_integrated(ctx, resolved_deps, id, dep)
        elif dep.source == Source.download:
            return self.resolve_download(ctx, resolved_deps, id, dep)
        elif dep.source == Source.smithed:
            return self.resolve_smithed(ctx, resolved_deps, id, dep)
        else:
            raise ValueError(f"Unknown source {dep.source}")
    
    def resolve_smithed(self, ctx: Context, resolved_deps : list[WeldDep], id: str, dep: WeldDepOptions):
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
        resolved_deps.append(WeldDep(
            id=data["id"],
            name=version["name"],
            downloads=Downloads(**version["downloads"])
        ))
        for self_deps in version.get("dependencies", []):
            new_dep = WeldDepOptions(
                version=self_deps["version"],
                source=Source.smithed
            )
            self.resolve(ctx, resolved_deps, self_deps["id"], new_dep)


def remove_duplicates(resolved_deps : list[WeldDep]):
    new_deps = {}
    for dep in resolved_deps:
        if dep.id not in new_deps:
            new_deps[dep.id] = dep
        else:
            version_a = new_deps[dep.id].name
            version_b = dep.name
            version_a = semver.VersionInfo.parse(version_a)
            version_b = semver.VersionInfo.parse(version_b)
            if version_a < version_b:
                new_deps[dep.id] = dep
    return list(new_deps.values())
    


@configurable("weld_deps", validator=WeldDepsConfig)
def beet_default(ctx: Context, opts: WeldDepsConfig):
    if not opts.enabled:
        return
    weld.toolchain.main.weld(ctx)
    
    resolved_deps : list[WeldDep] = []
    for id, dep in opts.deps.items():
        opts.resolve(ctx, resolved_deps, id, dep)
    resolved_deps = remove_duplicates(resolved_deps)
    resolved_deps.sort(key=lambda x: x.name)
    for dep in resolved_deps:
        rp, dp = dep.download(ctx)
        if rp:
            ctx.require(weld.toolchain.main.subproject_config(weld.toolchain.main.PackType.ASSETS, str(rp)))       
        if dp:
            ctx.require(weld.toolchain.main.subproject_config(weld.toolchain.main.PackType.DATA, str(dp)))         

