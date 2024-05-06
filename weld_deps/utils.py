import requests
import semver
from typing import Union
from pprint import pprint


from smithed import weld
from beet import Context, DataPack, ResourcePack


from .dep import VersionedDep, Dep, Source, get_id_slug


"""
Utility functions
"""


def get_filename(dep: VersionedDep, pack_type) -> str:
    return f"{dep.identifier}-{pack_type}.zip"


def get_identifier(dep: VersionedDep) -> str:
    return f"{dep.id}@{dep.source}"


def get_dict_identifier(dep: dict):
    return f'{dep["id"]}@{dep["source"]}#{dep["match"]}'


"""
Working with deps
"""


def parse_deps(deps: list[dict]) -> dict[Dep, list[str]]:
    result = {}
    for d in deps:
        id, slug = get_id_slug(d["id"], Source(d["source"]))
        dep = Dep(id=id, source=Source(d["source"]), slug=slug)
        match = d["match"].split(",")
        match = [m.strip() for m in match]
        result[dep] = match
    return result


def resolve_deps(deps: dict[Dep, list[str]], include_prerelease: bool) -> list[VersionedDep]:
    new_deps = dict()
    for dep in deps:
        # sort versions by semver
        versions = sorted(
            dep.get_versions(),
            key=lambda v: semver.VersionInfo.parse(v.version.lstrip("v")),
            reverse=True,
        )
        if not include_prerelease:
            versions = [
                v
                for v in versions
                if not semver.VersionInfo.parse(v.version.lstrip("v")).prerelease
            ]
            versions = [
                v 
                for v in versions 
                if not semver.VersionInfo.parse(v.version.lstrip("v")).build
            ]

        # filter versions by match
        versions = [v for v in versions if all([semver.match(v.version.lstrip("v"), deps[dep][i]) for i in range(len(deps[dep]))])]
        # append newest version
        if len(versions) == 0:
            raise ValueError(f"Could not find a version for {dep.slug} that matches the requirements: {deps[dep]}, available versions: {', '.join([v.version for v in dep.get_versions()])}")
        new_deps[get_identifier(versions[0])] = versions[0]
        # append dependencies
        add_deps(versions[0], new_deps)
    return new_deps.values()


def add_deps(dep: VersionedDep, deps: dict[str, VersionedDep]):
    for d in dep.dependencies:
        id_d = get_identifier(d)
        if id_d not in deps:
            deps[id_d] = d
        elif semver.VersionInfo.parse(deps[id_d].version) < semver.VersionInfo.parse(
            d.version
        ):
            deps[id_d] = d
        if len(d.dependencies) > 0:
            add_deps(d, deps)


"""
Caching
"""


def load_deps(
    ctx: Context, files: list[str], clean_load_tag: bool, enable_weld_merging: bool
):
    if enable_weld_merging:
        weld.toolchain.main.weld(ctx)
    cache_dir = ctx.cache.path / "weld_deps"

    for file in files:
        if file.endswith("dp.zip"):
            data = DataPack(zipfile=cache_dir / file)
            data = clean_pack(ctx, data, clean_load_tag)
            ctx.data.merge(data)
        elif file.endswith("rp.zip"):
            resource = ResourcePack(zipfile=cache_dir / file)
            resource = clean_pack(ctx, resource, clean_load_tag)
            ctx.assets.merge(resource)


def cache_deps(ctx: Context, deps: list[VersionedDep]):
    cache_dir = ctx.cache.path / "weld_deps"
    cache_dir.mkdir(exist_ok=True)

    result = []
    result_urls = []

    for dep in deps:
        datapack_id = get_filename(dep, "dp")
        datapack_path = cache_dir / datapack_id
        resourcepack_id = get_filename(dep, "rp")
        resourcepack_path = cache_dir / resourcepack_id

        if dep.datapack_download_url and dep.datapack_download_url.startswith(
            "https://"
        ):
            if not datapack_path.exists():
                datapack = dep.get_datapack()
                datapack_path.write_bytes(datapack)
            result.append(get_filename(dep, "dp"))
            result_urls.append(dep.datapack_download_url)
        if dep.resourcepack_download_url and dep.resourcepack_download_url.startswith(
            "https://"
        ):
            if not resourcepack_path.exists():
                resourcepack = dep.get_resourcepack()
                resourcepack_path.write_bytes(resourcepack)
            result.append(get_filename(dep, "rp"))
            result_urls.append(dep.resourcepack_download_url)
    return result, result_urls


def download_from_urls(ctx: Context, urls: list[str], files: list[str]):
    cache_dir = ctx.cache.path / "weld_deps"
    cache_dir.mkdir(exist_ok=True)

    for url, file in zip(urls, files):
        path = cache_dir / file
        if not path.exists():
            path.write_bytes(requests.get(url).content)


def clean_pack(
    ctx: Context, pack: Union[DataPack, ResourcePack], clean_load_tag: bool
) -> Union[DataPack, ResourcePack]:
    if "pack.png" in pack.extra:
        del pack.extra["pack.png"]
    if (
        isinstance(pack, DataPack)
        and "load:load" in pack.function_tags
        and clean_load_tag
    ):
        del pack.function_tags["load:load"]
    return pack
