import sys
import airflow
from airflow import DAG, macros
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime, timedelta

# Would be cleaner to add the path to the PYTHONPATH variable
sys.path.insert(1, '/usr/local/airflow/dags/scripts')

from process_logs import process_logs_func

class CustomPostgresOperator(PostgresOperator):
    template_fields = ('sql', 'parameters')

default_args = {
            "owner": "Airflow",
            "start_date": datetime(2019, 7, 29),
            "depends_on_past": False,
            "email_on_failure": False,
            "email_on_retry": False,
            "email": "youremail@host.com",
            "retries": 1
        }

templated_log_dir = """{{ var.value.source_path }}/data/{{ macros.ds_format(ts_nodash, "%Y%m%dT%H%M%S", "%Y-%m-%d-%H-%M") }}/"""

with DAG(dag_id="macro_and_template", schedule_interval="*/10 * * * *", default_args=default_args) as dag:

    # Notice that passing templated_log_dir to params won't have any effects
    # templated_log_dir won't be templated in the script generate_new_logs.sh
    # as params is not a template_fields.
    t1 = BashOperator(
            task_id="generate_new_logs",
            bash_command="./scripts/generate_new_logs.sh",
            params={'filename': 'log.csv', 'no_effect': templated_log_dir})

    t2 = BashOperator(
            task_id="logs_exist",
            bash_command="test -f " + templated_log_dir + "log.csv",
            )

    t3 = PythonOperator(
            task_id="process_logs",
            python_callable=process_logs_func,
            provide_context=True,
            templates_dict={'log_dir': templated_log_dir},
            params={'filename': 'log.csv'}
            )

    t4 = CustomPostgresOperator(
            task_id="save_logs",
            sql="./scripts/insert_log.sql",
            parameters={'log_dir': templated_log_dir}
            )


    t1 >> t2 >> t3 >> t4