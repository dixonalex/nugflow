from typing import List, Set
from dataclasses import dataclass, fields
from pathlib import Path
import pandas as pd

data_marker_missing_value = "9" * 32


@dataclass
class VaultData:
    table_name: str
    hkey_columns: List[str]
    data: pd.DataFrame
    sys_cols = ["source_service", "load_date"]

    @property
    def staged_table_name(self) -> str:
        load_date = self.data["load_date"].iloc[0].replace("-", "")
        return f"_{load_date[:10]}_{self.table_name}"

    @property
    def attribute_columns(self) -> Set[str]:
        all_cols = list(self.data)
        non_attr_cols = {"hkey", *self.hkey_columns, *self.sys_cols}
        cols = set(all_cols) - non_attr_cols
        return cols

    @classmethod
    def from_csv(cls, path: str) -> "VaultData":
        df = pd.read_csv(path, index_col=False)
        stem = path.rsplit(".", 1)[0]
        tbl_name, chunk = stem.rsplit("_", 1)
        try:
            int(chunk)
        except ValueError:
            tbl_name = stem
        return cls(tbl_name, ["license_number"], df)

    def to_csv(self, dir: Path, chunk: int = 0) -> str:
        dst_path = dir.joinpath(self.table_name + f"_{chunk}.csv")
        self.data.to_csv(dst_path, index=None)
        return str(dst_path)
