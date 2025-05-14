from airflow.decorators import dag, task # type:ignore
from pendulum import datetime # type: ignore
from time import sleep


@dag(start_date=datetime(2025, 1, 1), schedule=None, catchup=False)
def celery():

    @task
    def a():
        print("A")
        sleep(15)


    @task
    def b():
        print("B")
        sleep(15)


    @task
    def c():
        print("C")
        sleep(15)


    @task
    def d():
        print("D")
        sleep(15)


    a() >> [b(), c(), d()]

celery()