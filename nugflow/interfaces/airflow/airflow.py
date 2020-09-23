from datetime import datetime
import os
import typing

from airflow import DAG
from airflow.models import TaskInstance, Variable
from airflow.operators.python_operator import PythonOperator

import nugflow.settings as s


def get_task_path(context: dict) -> str:
    """Return a relative processing dir path from an airflow context
    
        Example:
            $ {{ ti.dag_id }}/{{ ti.task_id }}/{{ ts }}/{{ ti.try_number }}
    """
    dag_id = context["ti"].dag_id
    task_id = context["ti"].task_id
    ts = context["ts"]
    try_number = context["ti"].try_number
    etl_path = f"{dag_id}/{task_id}/{ts}/{try_number}"
    task_path = os.path.join(s.DATA_PATH, etl_path)
    return task_path


def get_last_task_xcom(context: dict) -> typing.Any:
    ti: TaskInstance = context["ti"]
    task_ids = list(ti.task.upstream_task_ids)[0]
    print("task_ids", task_ids)
    xcoms = ti.xcom_pull(task_ids=task_ids)
    print("Got", xcoms)
    return xcoms


def get_dag_variable(context: dict, var_name: str) -> typing.Any:
    dag_id = context["dag"].dag_id
    key = f"{dag_id.upper()}_{var_name.upper()}"
    val = Variable.get(key)
    print("Got", val, "from", key)
    return val


class NugflowOperator(PythonOperator):
    def __init__(self, python_callable: typing.Callable, *args, **kwargs):
        super().__init__(
            task_id=python_callable.__name__,
            provide_context=True,
            python_callable=python_callable,
            *args,
            **kwargs,
        )


class NugflowManualDAG(DAG):
    default_args = {
        "owner": "airflow",
        "depends_on_past": True,
        "start_date": datetime(2015, 6, 1),
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 0,
    }

    def __init__(self, dag_id: str):
        super().__init__(
            dag_id,
            schedule_interval=None,
            catchup=False,
            default_args=self.default_args,
        )
