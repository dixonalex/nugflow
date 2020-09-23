import os
import pandas as pd
import pytest
import typing

# https://docs.pytest.org/en/latest/plugins.html#requiring-loading-plugins-in-a-test-module-or-conftest-file
pytest_plugins = "fixtures.illinois"


def bootstrap_test() -> None:
    """Bootstrap the system with test configuration"""
    os.environ["VAULT_DB_NAME"] = "test.db"
    from nugflow.config import bootstrap

    bootstrap()


@pytest.fixture(autouse=True, scope="session")
def init_test_db() -> typing.Generator[None, None, None]:
    """Creates a sqlite3 database"""
    bootstrap_test()
    try:
        import alembic.config

        args = ["-n", "test", "--raiseerr", "upgrade", "head"]
        alembic.config.main(argv=args)
        yield
    finally:
        os.remove("test.db")


@pytest.fixture()
def liquor_license_illinois_sat_data() -> pd.DataFrame:
    """Some mock data"""
    return pd.DataFrame(
        data={
            "hkey": ["12345"],
            "load_date": ["01/01/2019"],
            "source_service": [__name__],
            "hash_diff": ["mock_data"],
            "license_number": ["mock_data"],
            "license_class": ["mock_data"],
            "retail_type": ["mock_data"],
            "sales_tax_account_number": ["mock_data"],
            "issue_date": ["mock_data"],
            "expiration_date": ["mock_data"],
            "application_status": ["mock_data"],
            "license_status": ["mock_data"],
            "licensee_name": ["mock_data"],
            "business_name": ["mock_data"],
            "street_address": ["123 Green St"],
            "city": ["Chicago"],
            "state": ["IL"],
            "zip": ["60642"],
            "county": ["Cook"],
            "type": ["mock_data"],
            "owners": ["mock_data"],
        }
    )
