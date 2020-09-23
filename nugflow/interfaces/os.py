import pickle
from pathlib import Path
import os
import shutil
from typing import Any, Collection, Generator, List


def copy_file(src: str, dst: str) -> None:
    dst_path = Path(dst)
    if not dst_path.exists():
        os.makedirs(str(Path(dst).parent), exist_ok=True)
        shutil.copy(src, dst)


def walk(paths: List[str]) -> Generator[str, None, None]:
    """Walk a directory and all sub-directories"""
    try:
        path = Path(paths.pop())
    except IndexError:
        return
    if path.is_dir():
        for sub_path in path.iterdir():
            yield from walk([str(sub_path)])
    else:
        yield str(path.resolve())


def apply_manifest(data: Any, uri: Path) -> str:
    manifest_path = uri.parent.joinpath("manifest.json")
    with open(manifest_path, mode="a") as f:
        print(data)
    return "oops"


def put(data: Any, dst: str) -> str:
    """Put any data to file system, return path"""
    # pickle.dumps(data, dst)
    return "manifest.json"


def put_many(data: Collection[Any], dst: str) -> str:
    for datum in data:
        put(datum, dst)
    return "foo"
