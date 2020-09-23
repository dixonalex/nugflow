from datetime import datetime
import inject
import pandas as pd
from nugflow.interfaces.vault import VaultData, df_to_vault
from nugflow.interfaces.db import Db


@inject.autoparams("db")
def lookup_license_numbers(df: pd.DataFrame, db: Db) -> pd.DataFrame:
    staged_tbl = f"_{str(id(df))}_license_lkp"
    try:
        df.to_sql(staged_tbl, db.conn, index=False)
        df_lkp = db.get_df(
            f"SELECT t.*, h.license_number FROM {staged_tbl} t"
            f" JOIN liquor_license_hub h ON h.hkey = t.hkey;"
        )
        return df_lkp
    finally:
        for table in db.get_tables():
            if table.endswith("_license_lkp"):
                print("Dropping", table)
                db.run_drop(table)


def get_vault_geocode(path: str, date: str = datetime.now().isoformat()) -> VaultData:
    df = pd.read_csv(
        path,
        encoding="ISO-8859-1",
        header=None,
        names=[
            "hkey",
            "full_address",
            "match_type",
            "match_exactness",
            "full_address_calculated",
            "latlon",
            "tiger_line_id",
            "tiger_line_side",
        ],
    )
    df = lookup_license_numbers(df)
    df[["longitude", "latitude"]] = df["latlon"].str.split(",", n=1, expand=True)
    del df["latlon"]
    print(df.head())

    tbl_metadata = [
        (list(df), ["license_number"], "liquor_license_geolocation_sat"),
    ]

    return df_to_vault(df, date, __name__, tbl_metadata)[0]


if __name__ == "__main__":
    print("hiya!")
    from nugflow.config import bootstrap

    bootstrap()
    vd = get_vault_geocode(
        "./airflow/data/processing/nugflow_alcohol_vault_to_mart/extract_address_geocodes/2019-11-30T03:42:49.885607+00:00/2/geocode_35.csv"
    )
    print(vd.data.head())
