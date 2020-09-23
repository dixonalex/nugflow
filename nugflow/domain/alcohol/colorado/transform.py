import os

import inject
import pandas as pd
import typing

from nugflow.interfaces.repo import DataRepo
from nugflow.interfaces.vault import VaultData, df_to_vault


@inject.autoparams("repo")
def transform(
        manifest_path: str,
        target_path: str,
        timestamp: str,
        repo: DataRepo
) -> str:
    paths = list()
    for entry in repo.read_manifest(manifest_path)["entries"]:
        path = entry["url"]
        df = pd.read_csv(path)
        print(df.head())
        vault_containers = build_dfs(df, timestamp)
        for vault_data in vault_containers:
            dst_path = os.path.join(target_path, vault_data.table_name + ".csv")
            vault_data.data.to_csv(dst_path, index=None)
            paths.append(str(dst_path))
    return repo.write_manifest(paths)


def build_dfs(df: pd.DataFrame, timestamp: str) -> typing.Iterable[VaultData]:
    source_service = __name__
    col_rename = {"expiration": "expires"}

    hkey_cols = ["license_number"]
    hub_cols = hkey_cols
    sat_cols = hub_cols + [
        "licensee_name",
        "doing_business_as",
        "license_type",
        "expires",
        "street_address",
        "city",
        "state",
        "zip",
    ]

    tbl_metadata = [
        (hub_cols, hkey_cols, "liquor_license_hub"),
        (sat_cols, hkey_cols, "liquor_license_colorado_sat"),
    ]

    return df_to_vault(df, timestamp, source_service, tbl_metadata, col_rename)
