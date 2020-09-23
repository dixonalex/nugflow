from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from nugflow.config import bootstrap
from nugflow.interfaces.vault import VaultData
from nugflow.interfaces.airflow.decorators import extractor, transformer, loader
import nugflow.interfaces.vault.repository as repo
import nugflow.domain.alcohol.colorado as co

bootstrap()


@extractor
def extract(tgt_path: str) -> str:
    """Fetch the liquor license data."""
    return co.extract(tgt_path)


@transformer
def transform(
        timestamp: str,
        manifest_path: str,
        task_path: str,
) -> str:
    """Transform the raw data into vault shapes."""
    return co.transform(
        manifest_path,
        task_path,
        timestamp
    )


@loader
def load(manifest: dict) -> None:
    """Load it into the vault cap'n"""
    for entry in manifest["entries"]:
        data_path = entry["url"]
        print("Got src_path", data_path)
        data = VaultData.from_csv(data_path)
        repo.stage(data)
        repo.load(data)
        repo.clean_stage()


default_args = {
    "owner": "airflow",
    "depends_on_past": True,
    "start_date": datetime(2015, 6, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
}

dag = DAG(
    "nugflow_alcohol_colorado",
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
)

with dag:
    e = PythonOperator(task_id="extract", provide_context=True, python_callable=extract)
    t = PythonOperator(
        task_id="transform", provide_context=True, python_callable=transform
    )
    l = PythonOperator(task_id="load", provide_context=True, python_callable=load)
    e >> t >> l
