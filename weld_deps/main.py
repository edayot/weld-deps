from beet import Context, DataPack, ResourcePack
from smithed import weld
from pprint import pprint
from typing import Dict, Union
from semver import VersionInfo
from .dep import Dep, Version, Source
import pathlib

        


def parse_deps(deps: list[dict]) -> dict[Dep, str]:
    return {
        Dep(id=d["id"], source=Source(d["source"])): d["match"]
        for d in deps
    }

def get_identifier(dep: Dep, version: Version, pack_type) -> str:
    return f"{dep.identifier}-{version.version}-{pack_type}.zip"



def beet_default(ctx: Context):
    deps = ctx.meta.get("weld_deps", {}).get("deps", [])
    if len(deps) == 0:
        return
    deps = parse_deps(deps)


    resolved_deps = resolve_dep(deps)

    cache_deps(ctx, resolved_deps)

    load_deps(ctx, resolved_deps)


def clean_pack(ctx : Context, pack: Union[DataPack, ResourcePack]) -> Union[DataPack, ResourcePack]:
    if "pack.png" in pack.extra:
        del pack.extra["pack.png"]
    if isinstance(pack, DataPack) and "load:load" in pack.function_tags and ctx.meta["weld_deps"].get("clean_load_tag", False):
        del pack.function_tags["load:load"]
    return pack




def load_deps(ctx : Context, deps: dict[Dep, Version]):
    weld.toolchain.main.weld(ctx)
    cache_dir = ctx.cache.path / "weld_deps"
    for dep, version in deps.items():
        datapack_id = get_identifier(dep, version, "dp")
        datapack_path = cache_dir / datapack_id
        if datapack_path.exists():
            data = DataPack(zipfile=datapack_path)
            data = clean_pack(ctx, data)
            ctx.data.merge(data)
        resourcepack_id = get_identifier(dep, version, "rp")
        resourcepack_path = cache_dir / resourcepack_id
        if resourcepack_path.exists():
            resource = ResourcePack(zipfile=resourcepack_path)
            resource = clean_pack(ctx, resource)
            ctx.assets.merge(resource)
            
    
def cache_deps(ctx : Context, deps: dict[Dep, Version]):
    cache_dir = ctx.cache.path / "weld_deps"
    cache_dir.mkdir(exist_ok=True)
    
    for dep, version in deps.items():
        datapack_id = get_identifier(dep, version, "dp")
        datapack_path = cache_dir / datapack_id
        if (
            not datapack_path.exists() and 
            (version.datapack_download_url and version.datapack_download_url.startswith("https://"))
        ):
            datapack = version.get_datapack()
            datapack_path.write_bytes(datapack)
        resourcepack_id = get_identifier(dep, version, "rp")
        resourcepack_path = cache_dir / resourcepack_id
        if (
            not resourcepack_path.exists() and 
            (version.resourcepack_download_url and version.resourcepack_download_url.startswith("https://"))
        ):
            resourcepack = version.get_resourcepack()
            resourcepack_path.write_bytes(resourcepack)


def resolve_dep(dist: Dict[Dep, str], max_recursion : int = 256) -> Dict[Dep, Version]:
    if max_recursion == 0:
        raise RecursionError("Max recursion reached")
    resolved_deps = {}

    for dep, version_expr in dist.items():
        available_versions = dep.get_available_versions(version_expr)

        if not available_versions:
            raise RuntimeError(f"No available versions for dependency {dep.identifier}")

        # Choose the highest version that matches the version expression
        matching_version = max(available_versions, key=lambda v: VersionInfo.parse(v.version))

        # Recursively resolve dependencies for the chosen version
        resolved_deps[dep] = matching_version
        resolved_deps.update(resolve_dep(matching_version.dependencies, max_recursion=max_recursion - 1))

    return resolved_deps