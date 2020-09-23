import inject
import nugflow.settings as s
from nugflow.interfaces.db import Db, SqliteDb, DbConfigProvider
from nugflow.interfaces.repo import DataRepo, LocalDataRepo, S3DataRepo


def configure(binder: inject.Binder) -> None:
    binder.bind(DbConfigProvider, DbConfigProvider(s.VAULT_DB_NAME))
    binder.bind_to_constructor(Db, lambda: SqliteDb())
    binder.bind_to_constructor(SqliteDb, lambda: SqliteDb())
    print(s.DATA_PATH)
    binder.bind(DataRepo, S3DataRepo() if s.DATA_PATH.startswith("s3") else LocalDataRepo())


def bootstrap() -> None:
    inject.clear_and_configure(configure)
