import os

import pytest
from pytest_insta import SnapshotFixture
from beet import run_beet, PluginError, ProjectConfig, DataPack, ResourcePack
from beet.contrib.unknown_files import UnknownData

from weld_deps.main import PackNotFoundError, PackVersionNotFoundError

EXAMPLES = [f for f in os.listdir("examples") if not f.startswith("nosnap_")]


def remove_unknown_files(pack: DataPack | ResourcePack):
    for path in set(pack[UnknownData].keys()):
        del pack[UnknownData][path]


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
            if isinstance(data_pack, DataPack):
                remove_unknown_files(data_pack)
            if isinstance(resource_pack, ResourcePack):
                remove_unknown_files(resource_pack)
            remove_unknown_files(ctx.data)
            remove_unknown_files(ctx.assets)

            assert data_pack == ctx.data
            assert resource_pack == ctx.assets