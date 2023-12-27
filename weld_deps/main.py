from beet import Context, DataPack, ResourcePack
from smithed import weld
from pprint import pprint
from typing import  Union
import semver
from .dep import Dep, Source, VersionedDep, get_id_slug
import pathlib
import itertools

        


def parse_deps(deps: list[dict]) -> dict[Dep, str]:
    result = {}
    for d in deps:
        id, slug = get_id_slug(d["id"], Source(d["source"]))
        dep = Dep(id=id, source=Source(d["source"]), slug=slug)
        match = d["match"]
        result[dep] = match
    return result

def get_filename(dep: VersionedDep, pack_type) -> str:
    return f"{dep.identifier}-{pack_type}.zip"

def get_identifier(dep: VersionedDep) -> str:
    return f"{dep.id}@{dep.source}"

def beet_default(ctx: Context):
    deps = ctx.meta.get("weld_deps", {}).get("deps", [])
    if len(deps) == 0:
        return
    deps = parse_deps(deps)

    deps = resolve_deps(deps)

    # cache deps
    cache_deps(ctx, deps)

    load_deps(ctx, deps)


def clean_pack(ctx : Context, pack: Union[DataPack, ResourcePack]) -> Union[DataPack, ResourcePack]:
    if "pack.png" in pack.extra:
        del pack.extra["pack.png"]
    if isinstance(pack, DataPack) and "load:load" in pack.function_tags and ctx.meta["weld_deps"].get("clean_load_tag", False):
        del pack.function_tags["load:load"]
    return pack




def load_deps(ctx : Context, deps: list[VersionedDep]):
    weld.toolchain.main.weld(ctx)
    cache_dir = ctx.cache.path / "weld_deps"
    for dep in deps:
        datapack_id = get_filename(dep, "dp")
        datapack_path = cache_dir / datapack_id
        if datapack_path.exists():
            data = DataPack(zipfile=datapack_path)
            data = clean_pack(ctx, data)
            ctx.data.merge(data)
        resourcepack_id = get_filename(dep, "rp")
        resourcepack_path = cache_dir / resourcepack_id
        if resourcepack_path.exists():
            resource = ResourcePack(zipfile=resourcepack_path)
            resource = clean_pack(ctx, resource)
            ctx.assets.merge(resource)
            
    
def cache_deps(ctx : Context, deps: list[VersionedDep]):
    cache_dir = ctx.cache.path / "weld_deps"
    cache_dir.mkdir(exist_ok=True)
    
    for dep in deps:
        datapack_id = get_filename(dep, "dp")
        datapack_path = cache_dir / datapack_id
        if (
            not datapack_path.exists() and 
            (dep.datapack_download_url and dep.datapack_download_url.startswith("https://"))
        ):
            datapack = dep.get_datapack()
            datapack_path.write_bytes(datapack)
        resourcepack_id = get_filename(dep, "rp")
        resourcepack_path = cache_dir / resourcepack_id
        if (
            not resourcepack_path.exists() and 
            (dep.resourcepack_download_url and dep.resourcepack_download_url.startswith("https://"))
        ):
            resourcepack = dep.get_resourcepack()
            resourcepack_path.write_bytes(resourcepack)


def resolve_deps(deps: dict[Dep, str]) -> list[VersionedDep]:
    new_deps = dict()
    for dep in deps:
        # sort versions by semver
        versions = sorted(dep.get_versions(), key=lambda v: semver.VersionInfo.parse(v.version), reverse=True)
        # filter versions by match
        versions = [v for v in versions if semver.match(v.version, deps[dep])]
        # append newest version
        new_deps[get_identifier(versions[0])] = versions[0]
        # append dependencies
        add_deps(versions[0], new_deps)
    return new_deps.values()

def add_deps(dep: VersionedDep, deps: set[VersionedDep]):
    for d in dep.dependencies:
        
        deps[get_identifier(d)] = d
        if len(d.dependencies) > 0:
            add_deps(d, deps)


