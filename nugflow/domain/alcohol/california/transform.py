from functools import singledispatch
import pandas as pd
import typing
import zipfile

from nugflow.interfaces.vault import VaultData, df_to_vault


@singledispatch
def transform(arg):
    print(arg)


@transform.register(str)
def _str(arg: str, date: str) -> typing.Iterable[VaultData]:
    path = arg
    with zipfile.ZipFile(path, "r") as zf:
        zf.extractall()
    with open("ABC_WeeklyDataExport.csv") as f:
        f.readline()
        df = pd.read_csv(f)
    print(df.head())
    return transform(df, date)


@transform.register(pd.DataFrame)
def _df(arg: pd.DataFrame, date: str) -> typing.Iterable[VaultData]:
    df = arg
    source_service = __name__
    col_rename = {"file_number": "license_number"}

    hkey_cols = ["license_number"]
    hub_cols = hkey_cols
    sat_cols = hub_cols + [
        "license_type",
        "lic_or_app",
        "type_status",
        "type_orig_iss_date",
        "expir_date",
        "master_ind",
        "term_in_#_of_months",
        "geo_code",
        "primary_name",
        "prem_addr_1",
        "prem_addr_2",
        "prem_city",
        "prem_state",
        "prem_zip",
        "dba_name",
        "prem_county",
        "prem_census_tract_#",
    ]

    tbl_metadata = [
        (hub_cols, hkey_cols, "liquor_license_hub"),
        (sat_cols, hkey_cols, "liquor_license_california_sat"),
    ]

    return df_to_vault(df, date, source_service, tbl_metadata, col_rename)


if __name__ == "__main__":
    transform("/home/alexanderldixon/downloads/data.csv.zip", "2019-11-29")
