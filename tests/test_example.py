import os

import pytest
from pytest_insta import SnapshotFixture
from beet import run_beet, PluginError, ProjectConfig, DataPack, ResourcePack, Pack, NamespaceFile

from weld_deps.main import PackNotFoundError, PackVersionNotFoundError

EXAMPLES = [f for f in os.listdir("examples") if not f.startswith("nosnap_")]


def remove_not_vanilla_namespacefile(pack: Pack):
    for namespace in pack.extend_namespace:
        for path in set(pack[namespace].keys()):
            del pack[namespace][path]


@pytest.mark.parametrize("directory", EXAMPLES)
def test_build(snapshot: SnapshotFixture, directory: str):

    if directory.startswith("fail_"):
        exception = directory.removeprefix("fail_")
        match exception:
            case "PackNotFoundError":
                real_exception = PackNotFoundError
            case "PackVersionNotFoundError":
                real_exception = PackVersionNotFoundError
            case _:
                raise ValueError(f"Unknown exception {exception}")
    
        with pytest.raises(real_exception):
            try:
                with run_beet(directory=f"examples/{directory}") as ctx:
                    pass
            except PluginError as e:
                cause = e.__cause__
                if not isinstance(cause, real_exception):
                    raise e from None
                raise cause from None
            
    else:
        with run_beet(directory=f"examples/{directory}") as ctx:
            data_pack = snapshot("data_pack")
            resource_pack = snapshot("resource_pack")
            remove_not_vanilla_namespacefile(ctx.data)
            remove_not_vanilla_namespacefile(ctx.assets)

            assert data_pack == ctx.data
            assert resource_pack == ctx.assets