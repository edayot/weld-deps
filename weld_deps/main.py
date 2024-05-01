from beet import Context
from pprint import pprint
from .utils import (
    get_dict_identifier,
    parse_deps,
    resolve_deps,
    cache_deps,
    download_from_urls,
    load_deps,
)


def beet_default(ctx: Context):

    if "weld_deps" not in ctx.meta:
        return
    if ctx.meta["weld_deps"].get("enabled", False) == False:
        return


    enable_weld_merging = ctx.meta["weld_deps"].get("enable_weld_merging", True)
    clean_load_tag = ctx.meta["weld_deps"].get("clean_load_tag", True)
    include_prerelease = ctx.meta["weld_deps"].get("include_prerelease", False)
    params = {
        "clean_load_tag": clean_load_tag,
        "enable_weld_merging": enable_weld_merging,
        "include_prerelease": include_prerelease,
    }

    deps = ctx.meta.get("weld_deps", {}).get("deps", [])
    deps = [d for d in deps if d["source"] != "integrated"]
    if len(deps) == 0:
        return
    # get a hash of the deps
    deps_hash = set()
    [deps_hash.add(get_dict_identifier(d)) for d in deps]

    # check if deps are cached
    if "weld_deps" in ctx.cache.json:
        cache = ctx.cache.json["weld_deps"]
        if "deps" in cache:
            if set(cache["deps"]) == deps_hash and cache["params"] == params:
                download_from_urls(ctx, cache["urls"], cache["files"])
                load_deps(ctx, cache["files"], clean_load_tag, enable_weld_merging)
                return

    deps = parse_deps(deps)

    deps = resolve_deps(deps, include_prerelease)

    # cache deps
    files, urls = cache_deps(ctx, deps)

    ctx.cache.json["weld_deps"] = {
        "deps": list(deps_hash),
        "params": params,
        "files": list(files),
        "urls": list(urls),
    }

    ctx.cache.json["weld_deps_installed"] = {dep.slug: dep.version for dep in deps}

    load_deps(ctx, files, clean_load_tag, enable_weld_merging)
