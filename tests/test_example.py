import os

import pytest
from pytest_insta import SnapshotFixture, Fmt
from beet import run_beet, PluginError, ProjectConfig, DataPack, ResourcePack, Pack, NamespaceFile
from beet.library.test_utils import ignore_name
from pathlib import Path
from typing import List, Type

from weld_deps.main import PackNotFoundError, PackVersionNotFoundError

EXAMPLES = [f for f in os.listdir("examples") if not f.startswith("nosnap_")]



def create_fmt(data_namespace: List[Type[NamespaceFile]], assets_namespace: List[Type[NamespaceFile]]):
    class FmtResourcePack(Fmt[ResourcePack]):
        extension = ".resource_pack"

        def load(self, path: Path) -> ResourcePack:
            return ignore_name(ResourcePack(path=path, extend_namespace=assets_namespace))

        def dump(self, path: Path, value: ResourcePack):
            value.save(path=path, overwrite=True)

    class FmtDataPack(Fmt[DataPack]):
        extension = ".data_pack"

        def load(self, path: Path) -> DataPack:
            return ignore_name(DataPack(path=path, extend_namespace=data_namespace))

        def dump(self, path: Path, value: DataPack):
            value.save(path=path, overwrite=True)


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
            create_fmt(ctx.data.extend_namespace, ctx.assets.extend_namespace)
            data_pack = snapshot("data_pack")
            resource_pack = snapshot("resource_pack")

            assert data_pack == ctx.data
            assert resource_pack == ctx.assets