from datetime import datetime
from os.path import join

from airflow.models import DAG
from operators.twitter_operator import TwitterOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.utils.dates import days_ago

ARGS = {
    "owner": "vinicius",
    "depends_on_past": False,
    "start_date": days_ago(5)
}
BASE_FOLDER = join("/opt/airflow/datalake/{stage}/twitter_aluraonline/{partition}")
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.00Z"
PARTITION_FOLDER = "extract_date={{ ds }}"

'''
print("***************[LOG VINI] DAG - 1")
with DAG(dag_id="twitter_dag", start_date=datetime.now()) as dag:
    print("***************[LOG VINI] DAG - 2")
    twitter_operator = TwitterOperator(
        task_id="twitter_aluraonline",
        query="AluraOnline",
        file_path=join(
            BASE_FOLDER.format(stage="bronze", partition=PARTITION_FOLDER),
            "AluraOnline_{{ ds_nodash }}.json"
        )
    )
    print("***************[LOG VINI] DAG - 3")
    twitter_transform = SparkSubmitOperator(
        task_id="transform_twitter_aluraonline",
        application=(
            "/opt/airflow/spark/transformation.py"
        ),
        name="twitter_transformation",
        application_args=[
            "--src",
            "/opt/airflow/datalake/bronze/twitter_aluraonline/extract_date=2021-07-23",
            "--dest",
            "/opt/airflow/datalake/silver/twitter_aluraonline",
            "--process-date",
            "{{ ds }}",
        ]
    )

    twitter_operator >> twitter_transform

'''
print("***************[LOG VINI] DAG - 1")
with DAG(dag_id="twitter_dag", 
        default_args=ARGS,
        schedule_interval="0 1 * * *",
        max_active_runs=1
        ) as dag:
    start_time = ("{{"
                f" execution_date.strftime('{ TIMESTAMP_FORMAT }') "
                "}}")
    print("***************[LOG VINI] DAG - 2", start_time)
    twitter_operator = TwitterOperator(
        task_id="twitter_aluraonline",
        query="AluraOnline",
        file_path=join(
            BASE_FOLDER.format(stage="bronze", partition=PARTITION_FOLDER),
            "AluraOnline_{{ ds_nodash }}.json"
        ),
        start_time=(
            "{{"
            f" (execution_date - macros.timedelta(days=1) - macros.timedelta(hours=3)).strftime('{ TIMESTAMP_FORMAT }') "
            "}}"
        ),
        end_time=(
            "{{"
            f" (next_execution_date - macros.timedelta(hours=3)).strftime('{ TIMESTAMP_FORMAT }') "
            "}}"
        )
    )
    print("***************[LOG VINI] DAG - 3")
    twitter_transform = SparkSubmitOperator(
        task_id="transform_twitter_aluraonline",
        application=(
            "/opt/airflow/spark/transformation.py"
        ),
        name="twitter_transformation",
        application_args=[
            "--src",
            BASE_FOLDER.format(stage="bronze", partition=PARTITION_FOLDER),
            "--dest",
            BASE_FOLDER.format(stage="silver", partition=""),
            "--process-date",
            "{{ ds }}",
        ]
    )

    twitter_operator >> twitter_transform
