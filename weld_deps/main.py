from beet import Context
from pprint import pprint
from .utils import (
    get_dict_identifier,
    parse_deps,
    resolve_deps,
    cache_deps,
    download_from_urls,
    load_deps
)
        




def beet_default(ctx: Context):
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



