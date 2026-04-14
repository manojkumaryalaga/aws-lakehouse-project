from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'manoj',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
    'email': 'manojkyalaga@gmail.com'
}

dag = DAG(
    'lakehouse_pipeline',
    default_args=default_args,
    description='NYC Taxi lakehouse pipeline',
    schedule_interval='0 0 * * *',
    start_date=datetime(2026, 1, 1),
    catchup=False
)

run_etl = PythonOperator(
    task_id='run_etl',
    python_callable=lambda: __import__('subprocess').run(
        ['python', 'scripts/etl.py'], check=True
    ),
    dag=dag
)

load_sqlite = PythonOperator(
    task_id='load_to_sqlite',
    python_callable=lambda: __import__('subprocess').run(
        ['python', 'scripts/load_to_sqlite.py'], check=True
    ),
    dag=dag
)

run_dbt = BashOperator(
    task_id='run_dbt_models',
    bash_command='cd /projects/lakehouse/lakehouse_sqlite && dbt run',
    dag=dag
)

run_etl >> load_sqlite >> run_dbt