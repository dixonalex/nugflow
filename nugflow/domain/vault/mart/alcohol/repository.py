import inject
import pandas as pd
import typing
from nugflow.interfaces.db import Db


@inject.autoparams("db")
def mart_liquor_license(db: Db) -> None:
    tbl = "mart_liquor_license"
    print("Count before:", tbl, db.get_count(tbl))
    db.execute(f"DELETE FROM {tbl};")

    def select_template(cols: typing.Dict[str, str], table: str) -> str:
        cols["llgs.match_type"] = "geo_match_type"
        cols["llgs.match_exactness"] = "geo_match_exactness"
        cols["llgs.latitude"] = "latitude"
        cols["llgs.longitude"] = "longitude"

        insert = "INSERT INTO mart_liquor_license "

        select = ", ".join([f"t.{col} AS {alias}" for col, alias in cols.items()])
        select = "SELECT " + select
        select = select.replace("t.NULL", "NULL")
        select = select.replace("t.llgs", "llgs")

        from_ = f""" FROM {table} t 
  LEFT JOIN liquor_license_geolocation_sat llgs
  ON t.hkey = llgs.hkey"""
        return insert + select + from_ + ";"

    base_cols = {
        "hkey": "id",
        "load_date": "load_date",
        "source_service": "source_service",
        "license_number": "license_number",
    }

    llils_cols = {
        **base_cols,
        "street_address": "address_1",
        "NULL": "address_2",
        "city": "city",
        "state": "state",
        "zip": "zip",
        "business_name": "doing_business_as",
        "expiration_date": "expiration_date",
    }

    sql = select_template(llils_cols, "liquor_license_illinois_sat")
    print(sql)
    db.execute(sql)

    llcos_cols = {
        **base_cols,
        "street_address": "address_1",
        "NULL": "address_2",
        "city": "city",
        "state": "state",
        "zip": "zip",
        "doing_business_as": "doing_business_as",
        "expires": "expiration_date",
    }

    sql = select_template(llcos_cols, "liquor_license_colorado_sat")
    db.execute(sql)

    llcas_cols = {
        **base_cols,
        "prem_addr_1": "address_1",
        "prem_addr_2": "address_2",
        "prem_city": "city",
        "prem_state": "state",
        "prem_zip": "zip",
        "dba_name": "doing_business_as",
        "expir_date": "expiration_date",
    }

    sql = select_template(llcas_cols, "liquor_license_california_sat")
    db.execute(sql)

    print("Count after:", tbl, db.get_count(tbl))


@inject.autoparams("db")
def get_geocode_input(db: Db) -> pd.DataFrame:
    tbl = "mart_liquor_license"
    print("Count:", tbl, db.get_count(tbl))
    df = db.get_df(
        f"""SELECT id, address_1, city, state, zip
 FROM mart_liquor_license
 WHERE geo_match_type IS NULL;"""
    )
    return df
