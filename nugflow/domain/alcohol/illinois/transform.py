from functools import singledispatch
import pandas as pd
import typing

from nugflow.interfaces.vault import VaultData, df_to_vault


def split_address(address: str) -> typing.List[str]:
    """Split a full address into its components

    Example:
        217 FRONT ST

        MCHENRY IL, 600505500

        Should return ['217 FRONT ST', 'MCHENRY', 'IL', '600505500']

    Returns:
        [str]: street_address, city, state, zip
    """
    street_address, *tail = address.split("\n")
    tail = [elem for elem in tail if elem]
    if isinstance(tail, list) and len(tail) > 1:
        address_2, *tail = tail
        street_address += " " + address_2
    tail = [elem for elem in tail if elem]
    city, state, _zip = tail[-1].rsplit(" ", 2)
    state = state.replace(",", "")

    return pd.Series([street_address, city, state, _zip])


@singledispatch
def transform(arg):
    print(arg)


@transform.register(str)
def _str(arg: str, date: str) -> typing.Iterable[VaultData]:
    df = pd.read_csv(arg)
    print(df.head())
    return transform(df, date)


@transform.register(pd.DataFrame)
def _df(arg: pd.DataFrame, date: str) -> typing.Iterable[VaultData]:
    df = arg
    source_service = __name__

    df[["street_address", "city", "state", "zip"]] = df["Address"].apply(split_address)
    col_rename = {"sales_tax_account_#": "sales_tax_account_number"}

    hkey_cols = ["license_number"]
    hub_cols = hkey_cols
    sat_cols = hub_cols + [
        "license_class",
        "retail_type",
        "sales_tax_account_number",
        "issue_date",
        "expiration_date",
        "application_status",
        "license_status",
        "licensee_name",
        "business_name",
        "street_address",
        "city",
        "state",
        "zip",
        "county",
        "type",
        "owners",
    ]

    tbl_metadata = [
        (hub_cols, hkey_cols, "liquor_license_hub"),
        (sat_cols, hkey_cols, "liquor_license_illinois_sat"),
    ]
    return df_to_vault(df, date, source_service, tbl_metadata, col_rename)


if __name__ == "__main__":
    transform(
        "/home/alexanderldixon/code/nugflow/airflow/data/processing/nugflow_alcohol_illinois/extract/2019-11-06T11:48:21.121006+00:00/5/data_2019-11-06.csv",
        "2019-11-13",
    )
