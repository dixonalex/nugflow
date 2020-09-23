from datetime import datetime
from pathlib import Path
import pytest

import nugflow.interfaces.airflow.airflow as sut


class TaskInstance:
    dag_id = "test_dag_id"
    task_id = "test_task_id"
    try_number = 2


@pytest.fixture()
def airflow_context() -> dict:
    return {"ti": TaskInstance(), "ts": datetime.now().isoformat()}


def test_get_work_dir(tmp_path: Path, airflow_context: dict):
    """
    GIVEN an airflow context
    WHEN I get a processing path
    THEN I should be able to combine it with another path
    """
    # Arrange
    # Act
    path = sut.get_task_path(airflow_context)
    # Assert
    assert tmp_path.joinpath(path)
