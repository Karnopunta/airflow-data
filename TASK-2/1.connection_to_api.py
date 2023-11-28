from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
import pendulum

def my_uri():
    from airflow.hooks.base import BaseHook
    print(f"Gender API URI ", BaseHook.get_connection("gender_api").get_uri())

def create_http_operator(task_id, endpoint, method, data):
    return SimpleHttpOperator(
        task_id=task_id,
        endpoint=endpoint,
        method=method,
        data=data,
        http_conn_id="gender_api",
        log_response=True,
        dag=dag
    )

nama_list = ["Musa", "Lia", "Rudi", "Siti"]

timezone = pendulum.timezone("Asia/Jakarta")

dag = DAG(
    dag_id='alterra_connection_to_api',
    schedule_interval=None,
    start_date=datetime(2022, 10, 21, tzinfo=timezone),
    catchup=False,
)

print_uri = PythonOperator(
    task_id="print_uri",
    python_callable=my_uri,
    dag=dag
)

get_statistic = create_http_operator(
    task_id="get_statistic",
    endpoint="/statistic",
    method="GET",
    data=None 
)

nama_operators = []
for nama in nama_list:
    task_id = f"identify_name_{nama.lower()}"
    operator = create_http_operator(
        task_id=task_id,
        endpoint="/gender/by-first-name-multiple",
        method="POST",
        data=f'{{"country": "ID", "locale": null, "ip": null, "first_name": "{nama}"}}'
    )
    nama_operators.append(operator)

get_statistic >> print_uri
print_uri >> nama_operators 
