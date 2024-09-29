from airflow import DAG
import pandas as pd
from datetime import datetime, timedelta
import random
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

start_date = datetime(2024, 9, 30)
default_args = {
    "owner": "mrh",
    "depends_on_past": False,
    "backfill": False,
    # 'start_date': start_date
}

num_rows = 50
output_file = "./account_dim_large_data.csv"

account_ids = []
account_types = []
statuses = []
customer_ids = []
balances = []
opening_dates = []


def generate_random_data(row_num):
    account_id = f"A{row_num:05d}"
    account_types = random.choice(["Savings", "Checking"])
    status = random.choice(["Active", "Inactive"])
    customer_id = f"C{random.randint(1,1000)}"
    balance = round(random.uniform(100.00, 10000.00))

    now = datetime.now()
    random_date = now - timedelta(days=random.randint(1, 365))
    opening_date_millis = int(random_date.timestamp() * 1000)

    return account_id, account_types, status, customer_id, balance, opening_date_millis


def generate_account_dim_data():
    row_num = 1
    while row_num <= num_rows:
        account_id, account_types, status, customer_id, balance, opening_date_millis = (
            generate_random_data(row_num)
        )
        account_ids.append(account_id)
        account_types.append(account_types)
        statuses.append(status)
        customer_ids.append(customer_id)
        balances.append(balance)
        opening_dates.append(opening_date_millis)
        row_num += 1

        df = pd.DataFrame(
            {
                "account_id": account_ids,
                "account_type": account_types,
                "status": statuses,
                "customer_id": customer_ids,
                "balance": balances,
                "opening_date": opening_dates,
            }
        )

        df.to_csv(output_file, index=False)

        print(f"{num_rows} rows of data generated and saved to {output_file}")


with DAG(
    "d_account_generator",
    default_args=default_args,
    description="Generate large account dimensions data in a CSV file",
    schedule_interval=timedelta(days=1),
    start_date=start_date,
    tags=["schema"],
) as dag:

    start = EmptyOperator(task_id="start_task")

    generate_account_dim_data = PythonOperator(
        task_id="generate_account_dim_data", python_callable=generate_account_dim_data
    )

    end = EmptyOperator(task_id="end_task")

    start >> generate_account_dim_data >> end
