from beet import Context, configurable
from pprint import pprint
from pydantic import BaseModel
from enum import Enum

class Source(str, Enum):
    integrated = "integrated"
    smithed = "smithed"

class WeldDep(BaseModel):
    id: str
    version: str
    source: Source


class WeldDepsConfig(BaseModel):
    enabled: bool = True
    enable_weld_merging: bool = True
    clean_load_tag: bool = True
    include_prerelease: bool = False
    deps: list[WeldDep] = []


@configurable("weld_deps", validator=WeldDepsConfig)
def beet_default(ctx: Context, opts: WeldDepsConfig):

    if not opts.enabled:
        return
    
    print(opts)

    