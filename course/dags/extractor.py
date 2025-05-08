from airflow.decorators import dag
from airflow.operators.python import PythonOperator # type: ignore
from pendulum import datetime

from include.datasets import DATASET_COCKTAIL
from include.tasks import _check_size, _get_cocktail


@dag(
    start_date=datetime(2025, 1, 1),
    schedule='@daily',
    catchup=False
)
def extractor():

    get_cocktail = PythonOperator(
        task_id = 'get_cocktail',
        python_callable = _get_cocktail,
        outlets = [DATASET_COCKTAIL]
    )

    check_size = PythonOperator(
        task_id = 'check_size',
        python_callable = _check_size
    )

    get_cocktail >> check_size

extractor()