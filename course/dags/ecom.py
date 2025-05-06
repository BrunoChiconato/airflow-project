from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator # type: ignore
from airflow.datasets import Dataset
from pendulum import datetime, duration


DATASET_COCKTAIL = Dataset('./tmp/cocktail.json')

@dag(
    start_date=datetime(2025, 1, 1),
    schedule=[DATASET_COCKTAIL],
    catchup=False,
    description='This DAG processes ecommerce data',
    tags=['course', 'ecom'],
    default_args={'retries': 1},
    dagrun_timeout=duration(minutes=20),
    max_consecutive_failed_dag_runs=2
)
def ecom():

    ta = EmptyOperator(task_id='ta')


ecom()
