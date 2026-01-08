try:
    from mecha import AstResourceLocation, Mecha, rule
except ImportError as e:
    raise ImportError(
        "weld_deps.contrib.mecha_auto_include requires mecha to be installed"
    ) from e
from beet import Context, Pack
from weld_deps.main import SmartDepOpts, Source
from typing import ClassVar


class PluginDepsHolder:
    ctx: ClassVar[Context]
    plugin_deps: ClassVar[list[SmartDepOpts]]

    @classmethod
    def get_smithed_id(cls, namespace: str):
        if namespace.startswith("bs."):
            return "bookshelf-" + namespace[3:]
        return {
            "itemio": "itemio",
            "smithed.actionbar": "actionbar",
            "smithed.crafter": "crafter",
            "smithed.custom_block": "custom-block",
            "smithed.title": "title",
            "energy": "energy",
        }.get(namespace)

    @classmethod
    def add_plugin_deps(cls, namespace: str):
        smithed_id = cls.get_smithed_id(namespace)
        if smithed_id is None:
            return
        cls.plugin_deps.append(
            SmartDepOpts(
                id=smithed_id,
                source=Source.smithed,
                version="latest",
            )
        )


@rule(AstResourceLocation)
def mecha_auto_include(node: AstResourceLocation):
    if node.namespace:
        PluginDepsHolder.add_plugin_deps(node.namespace)
    return node


def require(ctx: Context):
    mc = ctx.inject(Mecha)
    mc.transform.extend(mecha_auto_include)
    plugin_deps: list[SmartDepOpts] = ctx.meta.setdefault("weld_deps", {}).setdefault(
        "plugin_deps", []
    )
    PluginDepsHolder.plugin_deps = plugin_deps
    PluginDepsHolder.ctx = ctx


def pipeline(ctx: Context):
    packs: list[Pack] = [ctx.data, ctx.assets]
    for pack in packs:
        for namespace in pack.keys():
            PluginDepsHolder.add_plugin_deps(namespace)
