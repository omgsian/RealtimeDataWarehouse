from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from kafka_operator import KafkaProduceOperator

start_date = datetime(2024, 9, 15)
default_args = {
    "owner": "mrh",
    "depends_on_past": False,
    "backfill": False,
    "start_date": start_date,
}

with DAG(
    dag_id="f_transaction_generator",
    default_args=default_args,
    description="Transaction fact data generator",
    schedule_interval=timedelta(days=1),
    tags=["facts"],
) as dag:

    start = EmptyOperator(task_id="start")
    generate_txn_data = KafkaProduceOperator(
        task_id="generate_txn_data",
        kafka_broker="redpanda-0:9092",
        kafka_topic="transaction_facts",
        num_records=100,
    )
    end = EmptyOperator(task_id="end")

    start >> generate_txn_data >> end
