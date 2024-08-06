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

class WeldDepConfig(BaseModel):
    version: str
    source: Source = Source.smithed
    force_download_rp: Optional[str] = None
    force_download_dp: Optional[str] = None


class WeldDepsConfig(BaseModel):
    enabled: bool = True
    deps: dict[str, WeldDepConfig] = {}

    def resolve(self, ctx: Context, resolved_deps : list[WeldDep], id: str):
        dep = self.deps[id]
        if dep.source == Source.integrated:
            return
        elif dep.source == Source.download:
            dl : Downloads = {}
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
        for dep in version.get("dependencies", []):
            new_dep = WeldDepConfig(
                version=dep["version"],
                source=Source.smithed
            )
            self.deps[dep["id"]] = new_dep
            self.resolve(ctx, resolved_deps, dep["id"])


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
    for dep in set(opts.deps.keys()):
        opts.resolve(ctx, resolved_deps, dep)
    resolved_deps = remove_duplicates(resolved_deps)
    resolved_deps.sort(key=lambda x: x.name)
    for dep in resolved_deps:
        rp, dp = dep.download(ctx)
        if rp:
            ctx.require(weld.toolchain.main.subproject_config(weld.toolchain.main.PackType.ASSETS, str(rp)))       
        if dp:
            ctx.require(weld.toolchain.main.subproject_config(weld.toolchain.main.PackType.DATA, str(dp)))         

