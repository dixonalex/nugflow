from functools import wraps

import inject

from nugflow.interfaces.airflow.airflow import get_task_path, get_last_task_xcom
from nugflow.interfaces.repo import DataRepo


def extractor(f):
    @wraps(f)
    def wrapper(**context):
        work_dir = get_task_path(context)
        return f(work_dir)

    return wrapper


def transformer(f):
    @wraps(f)
    def wrapper(**context):
        timestamp = context["ts"]
        manifest_path = get_last_task_xcom(context)
        task_path = get_task_path(context)
        return f(timestamp, manifest_path, task_path)

    return wrapper


@inject.autoparams("repo")
def loader(f, repo: DataRepo):
    @wraps(f)
    def wrapper(**context):
        manifest_path = get_last_task_xcom(context)
        manifest = repo.read_manifest(manifest_path)
        return f(manifest)

    return wrapper
