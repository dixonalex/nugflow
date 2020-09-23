from pathlib import Path
from shutil import copyfile

import pytest


@pytest.fixture()
def path_to_illinois_extract(tmp_path: Path) -> str:
    file_name = "illinois_extract_11062019.csv"
    src_file_path = Path(__file__).parent.joinpath(file_name)
    dst_file_path = tmp_path.joinpath(file_name)
    copyfile(src_file_path, dst_file_path)
    return str(dst_file_path)
