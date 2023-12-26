
from enum import Enum
from dataclasses import dataclass
import requests
import semver


class Version():
    def __init__(self,
        id: str,
        version: str,
        datapack_download_url: str | None = None,
        resourcepack_download_url: str | None = None,
        dependencies: dict["Dep", str] = {}
    ):
        self.id = id
        self.version = version
        self.datapack_download_url = datapack_download_url
        self.resourcepack_download_url = resourcepack_download_url
        self.dependencies = dependencies

    def get_datapack(self) -> bytes:
        r = requests.get(self.datapack_download_url)
        r.raise_for_status()
        return r.content
    
    def get_resourcepack(self) -> bytes:
        r = requests.get(self.resourcepack_download_url)
        r.raise_for_status()
        return r.content


class Source(Enum):
    SMITHED = "smithed"
    MODRINTH = "modrinth"

class Dep():
    def __init__(self, id: str, source: Source, **kwargs):
        uid = self.get_uid(id, source)
        self.id = uid
        self.source : Source = source
    
    def get_uid(self, id, source : Source = None) -> str:
        if source is None:
            source = self.source
        
        if id in UID_MAP:
            return UID_MAP[id]
        elif source == Source.SMITHED:
            r = requests.get(f"https://api.smithed.dev/v2/packs/{id}/meta")
            r.raise_for_status()
            d = r.json()
            raw_id = d["rawId"]
            uid = d["docId"]
            UID_MAP[raw_id] = uid
            UID_MAP[uid] = uid
            return uid
        else:
            raise NotImplementedError("Modrinth is not yet supported")
    
    @property
    def versions_url(self) -> str:
        if self.source == Source.SMITHED:
            return f"https://api.smithed.dev/v2/packs/{self.id}/versions"
        elif self.source == Source.MODRINTH:
            raise NotImplementedError("Modrinth is not yet supported")

    @property
    def identifier(self) -> str:
        return f"{self.id}@{self.source}"
    
    def __hash__(self) -> int:
        return hash(self.identifier)

    def get_versions(self) -> list[str]:
        r = requests.get(self.versions_url)
        r.raise_for_status()
        versions = r.json()
        result = []
        for v in versions:
            v_dep = {}
            for dep in v["dependencies"]:
                dep_obj = Dep(id=dep["id"], source=Source.SMITHED)
                v_dep[dep_obj] = dep["version"]
            result.append(
                Version(
                    id=self.id,
                    version=v["name"],
                    datapack_download_url=v["downloads"]["datapack"] if "datapack" in v["downloads"] else None,
                    resourcepack_download_url=v["downloads"]["resourcepack"] if "resourcepack" in v["downloads"] else None,
                    dependencies=v_dep
                )
            )
        return result

    def get_available_versions(self, version_string) -> list[Version]:
        versions = self.get_versions()
        # parse pack_version string
        # filter versions
        return [
            v for v in versions
            if semver.VersionInfo.parse(v.version).match(version_string)
        ]

            

        
UID_MAP : dict[str, str] = {}
