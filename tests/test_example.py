import os

import pytest
from pytest_insta import SnapshotFixture
from beet import run_beet, PluginError

from weld_deps.main import PackNotFoundError, PackVersionNotFoundError

EXAMPLES = [f for f in os.listdir("examples") if not f.startswith("nosnap_")]


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
    
        with pytest.raises(PluginError):
            with run_beet(directory=f"examples/{directory}") as ctx:
                pass
    else:
        with run_beet(directory=f"examples/{directory}") as ctx:
            assert snapshot("data_pack") == ctx.data
            assert snapshot("resource_pack") == ctx.assets