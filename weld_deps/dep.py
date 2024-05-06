from enum import Enum
from dataclasses import dataclass
import requests
import semver
from typing import Dict, List
import itertools
from pydantic import BaseModel
from pprint import pprint

CACHED_VERSIONS: dict[str, List["VersionedDep"]] = {}

UID_MAP: dict[str, str] = {}
SLUG_MAP: dict[str, str] = {}


def get_id_slug(id: str, source: "Source") -> str:
    if id in UID_MAP:
        return UID_MAP[id], SLUG_MAP[id]
    elif source == Source.SMITHED:
        r = requests.get(f"https://api.smithed.dev/v2/packs/{id}/meta")
        r.raise_for_status()
        d = r.json()
        raw_id = d["rawId"]
        uid = d["docId"]
        UID_MAP[raw_id] = uid
        UID_MAP[uid] = uid
        SLUG_MAP[raw_id] = raw_id
        SLUG_MAP[uid] = raw_id
        return uid, raw_id
    elif source == Source.MODRINTH:
        r = requests.get(f"https://api.modrinth.com/v2/project/{id}")
        r.raise_for_status()
        d = r.json()
        slug = d["slug"]
        uid = d["id"]
        UID_MAP[slug] = uid
        UID_MAP[uid] = uid
        SLUG_MAP[slug] = slug
        SLUG_MAP[uid] = slug
        return uid, slug
    else:
        raise ValueError("Invalid source")


class Source(Enum):
    SMITHED = "smithed"
    MODRINTH = "modrinth"


class Dep(BaseModel):
    source: Source
    id: str
    slug: str

    @property
    def identifier(self) -> str:
        return f"{self.id}@{self.source}"

    def __hash__(self) -> int:
        return hash(self.identifier)

    @property
    def versions_url(self) -> str:
        if self.source == Source.SMITHED:
            return f"https://api.smithed.dev/v2/packs/{self.id}/versions"
        elif self.source == Source.MODRINTH:
            return f"https://api.modrinth.com/v2/project/{self.id}/version"

    def get_versions(self) -> List["VersionedDep"]:
        if self.identifier in CACHED_VERSIONS:
            return CACHED_VERSIONS[self.identifier]
        try:
            r = requests.get(self.versions_url)
            r.raise_for_status()
            versions = r.json()
        except requests.exceptions.HTTPError as e:
            raise ValueError(f"Failed to get versions for {self.identifier}, {e}")
        except e:
            raise e

        l_versions = []
        if self.source == Source.SMITHED:
            for v in versions:
                l_deps = []
                for dep in v["dependencies"]:
                    id, slug = get_id_slug(dep["id"], Source.SMITHED)
                    d_obj = Dep(
                        source=self.source,
                        id=id,
                        slug=slug,
                    )
                    d_obj_versions = d_obj.get_versions()
                    d_obj_version = [
                        v for v in d_obj_versions if v.version == dep["version"]
                    ][0]
                    l_deps.append(d_obj_version)

                v_obj = VersionedDep(
                    id=self.id,
                    slug=self.slug,
                    source=self.source,
                    version=v["name"],
                    dependencies=l_deps,
                    datapack_download_url=v["downloads"]["datapack"]
                    if "datapack" in v["downloads"]
                    else None,
                    resourcepack_download_url=v["downloads"]["resourcepack"]
                    if "resourcepack" in v["downloads"]
                    else None,
                )
                l_versions.append(v_obj)
        elif self.source == Source.MODRINTH:
            for v in versions:
                l_deps = []
                for dep in v["dependencies"]:
                    if dep["dependency_type"] == "optional":
                        continue
                    id, slug = get_id_slug(dep["project_id"], Source.MODRINTH)
                    d_obj = Dep(
                        source=self.source,
                        id=id,
                        slug=slug,
                    )
                    d_obj_versions = d_obj.get_versions()
                    if dep["version_id"] is None:
                        continue
                    d_obj_version = [
                        v for v in d_obj_versions if v.version_id == dep["version_id"]
                    ][0]
                    l_deps.append(d_obj_version)

                dp_url, rp_url = None, None
                for f in v["files"]:
                    if f["primary"]:
                        dp_url = f["url"]
                    elif f["file_type"] in [
                        "required-resource-pack",
                        "optional-resource-pack",
                    ]:
                        rp_url = f["url"]

                v_obj = VersionedDep(
                    id=self.id,
                    slug=self.slug,
                    source=self.source,
                    version=v["version_number"],
                    version_id=v["id"],
                    dependencies=l_deps,
                    datapack_download_url=dp_url,
                    resourcepack_download_url=rp_url,
                )
                l_versions.append(v_obj)
        CACHED_VERSIONS[self.identifier] = l_versions
        return l_versions


class VersionedDep(Dep):
    version: str
    dependencies: list["VersionedDep"]
    datapack_download_url: str | None
    resourcepack_download_url: str | None
    version_id: str | None = None

    @property
    def identifier(self) -> str:
        return f"{self.id}@{self.source}#{self.version}"

    def __hash__(self) -> int:
        return hash(self.identifier)

    def get_datapack(self) -> bytes:
        if self.datapack_download_url is None:
            raise ValueError("No datapack download url")
        r = requests.get(self.datapack_download_url)
        r.raise_for_status()
        return r.content

    def get_resourcepack(self) -> bytes:
        if self.resourcepack_download_url is None:
            raise ValueError("No resourcepack download url")
        r = requests.get(self.resourcepack_download_url)
        r.raise_for_status()
        return r.content
