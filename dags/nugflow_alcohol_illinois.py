# from datetime import datetime
# from pathlib import Path
# from typing import List
# from airflow import DAG
# from airflow.operators.python_operator import PythonOperator
#
# from nugflow.interfaces.airflow import (
#     get_work_dir,
#     get_last_task_xcom,
#     get_dag_variable,
# )
# from nugflow.config import bootstrap
# from nugflow.interfaces.os import copy_file, walk
# from nugflow.interfaces.vault import VaultData
# import nugflow.interfaces.vault.repository as repo
# import nugflow.domain.alcohol.illinois as il
#
#
# def extract(**context) -> List[str]:
#     """Fetch the liquor license data."""
#     dst_path = get_work_dir(context)
#     il.extract(dst_path)
#     return [str(dst_path)]
#
#
# def transform(**context) -> List[str]:
#     """Transform the raw data into vault shapes."""
#     dst_paths = list()
#     ts = context["ts"]
#     src_paths = get_last_task_xcom(context)
#     work_dir = get_work_dir(context)
#     for file_path in walk(src_paths):
#         print("Processing", file_path)
#         vault_data_list = il.transform(str(file_path), ts)
#         for vault_data in vault_data_list:
#             dst_path = vault_data.to_csv(work_dir)
#             dst_paths.append(str(dst_path))
#
#     return dst_paths
#
#
# def load(**context) -> None:
#     """Load it into the vault cap'n"""
#     src_paths = get_last_task_xcom(context)
#     bootstrap()
#     for src_path in src_paths:
#         print("Got src_path", src_path)
#         data = VaultData.from_csv(src_path)
#         repo.stage(data)
#         repo.load(data)
#         repo.clean_stage()
#
#
# default_args = {
#     "owner": "airflow",
#     "depends_on_past": True,
#     "start_date": datetime(2015, 6, 1),
#     "email_on_failure": False,
#     "email_on_retry": False,
#     "retries": 0,
# }
#
# dag = DAG(
#     "nugflow_alcohol_illinois",
#     schedule_interval=None,
#     catchup=False,
#     default_args=default_args,
# )
#
# with dag:
#     e = PythonOperator(task_id="extract", provide_context=True, python_callable=extract)
#     t = PythonOperator(
#         task_id="transform", provide_context=True, python_callable=transform
#     )
#     l = PythonOperator(task_id="load", provide_context=True, python_callable=load)
#     e >> t >> l
