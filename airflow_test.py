from airflow import DAG
from datetime import datetime

with DAG(
    "debug_test",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False
) as dag:

    broken_task = PythonOperator(
        task_id="broken_task",
        python_callable=lambda: print("Hello")
    )