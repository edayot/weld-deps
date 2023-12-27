from beet import Context, DataPack, ResourcePack
from smithed import weld
from pprint import pprint
from typing import  Union
import semver
from .dep import Dep, Source, VersionedDep, get_id_slug
import requests
import time
        


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

def get_dict_identifier(dep):
    return f'{dep["id"]}@{dep["source"]}#{dep["match"]}'

def beet_default(ctx: Context):
    t1 = time.perf_counter()
    deps = ctx.meta.get("weld_deps", {}).get("deps", [])
    if len(deps) == 0:
        return
    # get a hash of the deps
    deps_hash = set()
    [deps_hash.add(get_dict_identifier(d)) for d in deps]

    # check if deps are cached
    if "weld_deps" in ctx.cache.json:
        if "deps" in ctx.cache.json["weld_deps"]:
            if set(ctx.cache.json["weld_deps"]["deps"]) == deps_hash:
                download_from_urls(ctx, ctx.cache.json["weld_deps"]["urls"], ctx.cache.json["weld_deps"]["files"])
                load_deps(ctx, ctx.cache.json["weld_deps"]["files"])
                t2 = time.perf_counter()
                print(f"Execution time: {t2 - t1:0.4f} seconds")
                return

    deps = parse_deps(deps)

    deps = resolve_deps(deps)

    # cache deps
    files, urls = cache_deps(ctx, deps)

    ctx.cache.json["weld_deps"] = {
        "deps": list(deps_hash),
        "files": list(files),
        "urls": list(urls)
    }

    load_deps(ctx, files)
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")


def clean_pack(ctx : Context, pack: Union[DataPack, ResourcePack]) -> Union[DataPack, ResourcePack]:
    if "pack.png" in pack.extra:
        del pack.extra["pack.png"]
    if isinstance(pack, DataPack) and "load:load" in pack.function_tags and ctx.meta["weld_deps"].get("clean_load_tag", False):
        del pack.function_tags["load:load"]
    return pack




def load_deps(ctx : Context, files : list[str]):
    if ctx.meta["weld_deps"].get("enable_weld_merging", True):
        weld.toolchain.main.weld(ctx)
    cache_dir = ctx.cache.path / "weld_deps"

    for file in files:
        if file.endswith("dp.zip"):
            data = DataPack(zipfile=cache_dir / file)
            data = clean_pack(ctx, data)
            ctx.data.merge(data)
        elif file.endswith("rp.zip"):
            resource = ResourcePack(zipfile=cache_dir / file)
            resource = clean_pack(ctx, resource)
            ctx.assets.merge(resource)

    
def cache_deps(ctx : Context, deps: list[VersionedDep]):
    cache_dir = ctx.cache.path / "weld_deps"
    cache_dir.mkdir(exist_ok=True)

    result = []
    result_urls = []
    
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
        if dep.datapack_download_url and dep.datapack_download_url.startswith("https://"):
            result.append(get_filename(dep, "dp"))
            result_urls.append(dep.datapack_download_url)
        if dep.resourcepack_download_url and dep.resourcepack_download_url.startswith("https://"):
            result.append(get_filename(dep, "rp"))
            result_urls.append(dep.resourcepack_download_url)
    return result, result_urls

def download_from_urls(ctx : Context, urls: list[str], files: list[str]):
    cache_dir = ctx.cache.path / "weld_deps"
    cache_dir.mkdir(exist_ok=True)

    for url, file in zip(urls, files):
        path = cache_dir / file
        if not path.exists():
            path.write_bytes(requests.get(url).content)
        


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

def add_deps(dep: VersionedDep, deps: dict[str, VersionedDep]):
    for d in dep.dependencies:
        
        id_d = get_identifier(d)
        if id_d not in deps:
            deps[id_d] = d
        elif semver.VersionInfo.parse(deps[id_d].version) < semver.VersionInfo.parse(d.version):
            deps[id_d] = d
        if len(d.dependencies) > 0:
            add_deps(d, deps)


