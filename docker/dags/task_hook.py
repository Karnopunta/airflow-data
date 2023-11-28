from airflow import DAG
from datetime import datetime
from airflow.operators.postgres_operator import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python import PythonOperator

with DAG(
    dag_id='alterra_hook_task',
    schedule=None,
    start_date=datetime(2022, 10, 21),
    catchup=False
) as dag:
    create_table_in_db_task = PostgresOperator(
        task_id='create_table_in_db',
        sql=('CREATE TABLE IF NOT EXISTS gender_name_prediction ' +
             '(' +
             'first_name TEXT, ' +
             'country TEXT, ' +
             'credits_used FLOAT, ' +
             'duration TEXT, ' +
             'samples FLOAT, ' +
             'details_country TEXT, ' +
             'first_name_sanitized TEXT, ' +
             'result_found BOOLEAN, ' +
             'first_name_text TEXT, ' +
             'probability FLOAT, ' +
             'gender TEXT' +
             ')'),
        postgres_conn_id='pg_conn',
        autocommit=True,
        dag=dag
    )

    def load_data_to_postgres():
        pg_hook = PostgresHook(postgres_conn_id='pg_conn').get_conn()
        curr = pg_hook.cursor("cursor")
        with open('/opt/airflow/dags/df.csv', 'r') as file:
            next(file)
            curr.copy_from(file, 'gender_name_prediction', sep=',')
            pg_hook.commit()

    load_data_to_db_task = PythonOperator(
        task_id='load_data_to_db',
        python_callable=load_data_to_postgres,
        dag=dag
    )

    create_table_in_db_task >> load_data_to_db_task
