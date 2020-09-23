import abc
import dataclasses
import inject
import pandas as pd
import typing
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Connection


@dataclasses.dataclass
class DbConfigProvider:
    """Config values for database engine initialization
    :db_name (str): if using sqlite this should be the file path (e.g. 'nugflow.db')
    :in_memory (bool): will create an in memory instance, if possible
    """

    db_name: str
    in_memory: bool = False
    verbose: bool = False


class Db(abc.ABC):
    @property
    @abc.abstractmethod
    def conn(self) -> Connection:
        """Must implement a class returning a SQLAlchemy connection"""

    def execute(self, sql: str, *multiparams: typing.Any, **params: typing.Any) -> None:
        with self.conn.begin() as trans:
            with self.conn as con:
                con.execute(sql, *multiparams, **params)

    def get_records(self, sql: str) -> typing.List[tuple]:
        with self.conn as con:
            return [record for record in con.execute(sql)]

    def get_df(self, sql: str) -> pd.DataFrame:
        with self.conn as con:
            return pd.read_sql(sql, con)

    def get_count(self, tbl: str) -> int:
        """Get the count of rows for a given table name"""
        return self.get_records(f"SELECT COUNT(*) FROM {tbl};")[0][0]

    def get_record_exists(self, tbl: str, predicate: dict) -> bool:
        """True is predicate matches else record doesn't exist"""
        predicate_str = " AND ".join(
            [f"{col} = '{val}'" for col, val in predicate.items()]
        )
        ct = self.get_records(f"SELECT COUNT(*) FROM {tbl} WHERE {predicate_str};")[0][
            0
        ]
        return ct > 0

    def get_tables(self) -> typing.List[str]:
        """Get the tables under a database (assuming sqlite)"""
        return [
            r[0]
            for r in self.get_records(
                "SELECT name FROM sqlite_master WHERE type = 'table';"
            )
        ]

    def insert_records(self, tbl: str, data: pd.DataFrame) -> None:
        """Insert the dataframe into the given table"""
        data.to_sql(tbl, self.conn, if_exists="append", index=False)

    def run_drop(self, tbl: str) -> None:
        """Run a drop statement against a given table name"""
        self.execute(f"DROP TABLE IF EXISTS `{tbl}`;")

    def run_truncate(self, tbl: str) -> None:
        """Run a truncate statement against a given table name"""
        self.execute(f"DELETE FROM {tbl};")


class SqliteDb(Db):
    cfg = inject.attr(DbConfigProvider)

    def __init__(self) -> None:
        conn_str = (
            "sqlite://" if self.cfg.in_memory else f"sqlite:///{self.cfg.db_name}"
        )
        print("Connecting to", conn_str)
        self.engine = create_engine(conn_str, echo=self.cfg.verbose)

    @property
    def conn(self) -> Connection:
        return self.engine.connect()
