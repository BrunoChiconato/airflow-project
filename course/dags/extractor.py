from airflow.decorators import dag
from airflow.operators.python import PythonOperator # type: ignore
from pendulum import datetime, duration

from include.datasets import DATASET_COCKTAIL
from include.tasks import _check_size, _get_cocktail
from include.extractor.callbacks import (
    _handle_failed_dag_run,
    _handle_empty_size
)


@dag(
    start_date=datetime(2025, 1, 1),
    schedule='@daily',
    catchup=False,
    on_failure_callback=_handle_failed_dag_run,
    default_args={
        'retries': 2,
        'retry_delay': duration(seconds=2)
    },
    tags=['ecom']
)
def extractor():

    get_cocktail = PythonOperator(
        task_id = 'get_cocktail',
        python_callable = _get_cocktail,
        outlets = [DATASET_COCKTAIL],
        on_failure_callback=_handle_empty_size,
        retry_exponential_backoff=True,
        max_retry_delay=duration(minutes=15)
    )

    check_size = PythonOperator(
        task_id = 'check_size',
        python_callable = _check_size
    )

    get_cocktail >> check_size

extractor()