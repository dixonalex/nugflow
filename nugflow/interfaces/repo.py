import abc
from typing import AnyStr, List, Dict
import json

import s3fs


class DataRepo(abc.ABC):

    def write_manifest(self, paths: List[str]) -> str:
        """
        {
          "entries": [
            {"url":"s3://mybucket-alpha/2013-10-04-custdata"},
          ]
        }
        """
        manifest = {"entries": [{"url": path} for path in paths]}
        path = paths[0].rsplit("/", 1)[0] + "/manifest.json"
        print(path)
        self.write(path, json.dumps(manifest))
        return path

    def read_manifest(self, path: str) -> Dict:
        """
        {
          "entries": [
            {"url":"s3://mybucket-alpha/2013-10-04-custdata"},
          ]
        }
        """
        manifest = self.read(path)
        return json.loads(manifest)

    @abc.abstractmethod
    def write(self, path: str, data: AnyStr, mode: str = "w") -> None:
        pass

    @abc.abstractmethod
    def read(self, path: str, mode: str = "r") -> AnyStr:
        pass


class S3DataRepo(DataRepo):

    def __init__(self) -> None:
        self.fs = s3fs.S3FileSystem()
        super().__init__()

    def write(self, path: str, data: AnyStr, mode: str = "w") -> None:
        print("writing to", path)
        with self.fs.open(path, mode) as w:
            w.write(data)

    def read(self, path: str, mode: str = "r") -> AnyStr:
        with self.fs.open(path, mode) as r:
            return r.read()


class LocalDataRepo(DataRepo):

    def write(self, path: str, data: AnyStr, mode: str = "w") -> None:
        with open(path, mode) as w:
            w.write(data)

    def read(self, path: str, mode: str = "r") -> AnyStr:
        with open(path, mode) as r:
            return r.read()
