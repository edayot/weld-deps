from beet import Context, configurable, DataPack, ResourcePack
from pprint import pprint
from pydantic import BaseModel
from typing_extensions import TypedDict, NotRequired, Union, Optional
from enum import Enum
import json
import requests
import pathlib
from smithed import weld

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
    id: str
    version: str
    source: Source = Source.smithed
    download_rp: Optional[str] = None
    download_dp: Optional[str] = None

    def resolve(self, ctx: Context, resolved_deps : list[WeldDep]):
        if self.source == Source.integrated:
            return
        elif self.source == Source.download:
            resolved_deps.append(WeldDep(
                id=self.id,
                name=self.version,
                downloads={
                    "resourcepack": self.download_rp,
                    "datapack": self.download_dp
                }
            ))
            return
        url = f"https://api.smithed.dev/v2/packs/{self.id}"
        cache = ctx.cache["weld_deps"]
        path = cache.get_path(url)
        if not path.exists():
            response = requests.get(url)
            try:
                response.raise_for_status()
            except requests.HTTPError as e:
                raise ValueError(f"Pack {self.id} not found") from e
            path.write_text(response.text)
        data = json.loads(path.read_text())

        versions = filter(lambda x: x["name"] == self.version, data["versions"])
        versions = list(versions)
        if len(versions) == 0:
            raise ValueError(f"Version {self.version} of pack {self.id} not found")
        version = versions[0]
        resolved_deps.append(WeldDep(
            id=data["id"],
            name=version["name"],
            downloads=Downloads(**version["downloads"])
        ))
        for dep in version.get("dependencies", []):
            WeldDepConfig(
                id=dep["id"],
                version=dep["version"],
                source=Source.smithed
            ).resolve(ctx, resolved_deps)        


class WeldDepsConfig(BaseModel):
    enabled: bool = True
    deps: list[WeldDepConfig] = []


@configurable("weld_deps", validator=WeldDepsConfig)
def beet_default(ctx: Context, opts: WeldDepsConfig):
    if not opts.enabled:
        return
    weld.toolchain.main.weld(ctx)
    
    resolved_deps : list[WeldDep] = []
    for dep in opts.deps:
        dep.resolve(ctx, resolved_deps)
    for dep in resolved_deps:
        rp, dp = dep.download(ctx)
        if rp:
            ctx.require(weld.toolchain.main.subproject_config(weld.toolchain.main.PackType.ASSETS, rp))       
        if dp:
            ctx.require(weld.toolchain.main.subproject_config(weld.toolchain.main.PackType.DATA, dp))         

