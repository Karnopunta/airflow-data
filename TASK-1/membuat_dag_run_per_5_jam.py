from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator  #line 1-3 memnggil library yang digunakan

def print_hello():                               #membuat fungsi yang akan dijalankan
    return 'Hello world from first Airflow DAG!' #mengembalikan hasil/tampilan fungsi

dag = DAG(                                       #membuat dag
        'alterra_hello_world',                   #nama dag
        description='Hello World DAG',           #deskripsi/catatan dag
        schedule_interval='0 */5 * * *',         #dag yang berjalan setiap 5 jam sekali
        start_date=datetime(2022, 10, 21),       #dag mulai berjalan pada 21-10-2022
        catchup=False                            #Mengatur agar DAG tidak mengejar (catch up) pekerjaan yang terlewat
    )

operator_hello_world = PythonOperator(          #membuat fungsi operator
    task_id='hello_task',                       #nama task yang akan dijalankan oleh operator
    python_callable=print_hello,                #nama fungsi yang akan dijalankan oleh operator
    dag=dag                                     #menetapkan dag tempat tugas ini dijalankan
)

operator_hello_world                            #menjalankan perintah