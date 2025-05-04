from airflow.hooks.base import BaseHook
from airflow.exceptions import AirflowNotFoundException
from io import BytesIO
from include.helpers.minio import get_minio_client
import requests
import json


BUCKET_NAME = 'stock-market'

def _get_stock_prices(url: str, symbol: str):
    url = f'{url}{symbol}?metrics=high?&interval=1d&range=1y'
    api = BaseHook.get_connection('stock_api')

    response = requests.get(url, headers=api.extra_dejson['headers'])

    return json.dumps(response.json()['chart']['result'][0])


def _store_prices(stock):
    client = get_minio_client()

    if not client.bucket_exists(BUCKET_NAME):
        client.make_bucket(BUCKET_NAME)

    stock = json.loads(stock)
    symbol = stock['meta']['symbol']
    data = json.dumps(stock, ensure_ascii=False).encode('utf-8')

    objw = client.put_object(
        BUCKET_NAME,
        object_name=f'{symbol}/prices.json',
        data=BytesIO(data),
        length=len(data)
    )

    return f'{objw.bucket_name}/{symbol}'


def _get_formatted_csv(path: str):
    client = get_minio_client()
    prefix_name = f'{path.split('/')[1]}/formatted_prices/'
    objects = client.list_objects(
        BUCKET_NAME,
        prefix_name,
        recursive=True
    )

    for obj in objects:
        if obj.object_name.endswith('.csv'):
            return obj.object_name

    return AirflowNotFoundException('The csv file does not exist.')