import inject

from nugflow.interfaces.db import Db
from .entities import VaultData


@inject.autoparams("db")
def stage(vd: VaultData, db: Db) -> None:
    db.execute(f"DROP TABLE IF EXISTS {vd.staged_table_name};")
    db.execute(
        (
            f" CREATE TABLE {vd.staged_table_name} AS"
            f" SELECT * FROM {vd.table_name} WHERE 0;"
        )
    )
    vd.data.to_sql(vd.staged_table_name, db.conn, if_exists="append", index=False)
    print("Count loaded to staging", db.get_count(vd.staged_table_name))


@inject.autoparams("db")
def load(vd: VaultData, db: Db) -> None:
    where = (
        "tgt.hkey = src.hkey"
        if "_hub" in vd.table_name
        else "tgt.hkey = src.hkey AND tgt.hash_diff = src.hash_diff"
    )

    print("Count before:", vd.table_name, db.get_count(vd.table_name))

    sql = (
        f"INSERT INTO {vd.table_name}"
        f" SELECT DISTINCT * FROM {vd.staged_table_name} src"
        f" WHERE NOT EXISTS (SELECT * FROM {vd.table_name} tgt"
        f" WHERE {where});"
    )
    db.execute(sql)

    print("Count after:", vd.table_name, db.get_count(vd.table_name))


@inject.autoparams()
def clean_stage(db: Db) -> None:
    """Drop all tables that start with `_` (indicating a staging table)"""
    for table in db.get_tables():
        if table.startswith("_"):
            print(f"Dropping table {table}.")
            db.run_drop(table)
