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

num_rows = 100
output_file = "./customer_dim_large_data.csv"


def generate_random_data(row_num):
    customer_id = f"C{row_num:05d}"
    first_name = f"FirstName{row_num}"
    last_name = f"LastName{row_num}"
    email = f"customer{row_num}@example.com"
    phone_number = f"+1-800-{random.randint(1000000, 9999999)}"

    now = datetime.now()
    random_date = now - timedelta(days=random.randint(1, 365))
    registration_date_millis = int(random_date.timestamp() * 1000)

    return (
        customer_id,
        first_name,
        last_name,
        email,
        phone_number,
        registration_date_millis,
    )


customer_ids = []
first_names = []
last_names = []
emails = []
phone_numbers = []
registration_dates = []


def generate_customer_dim_data():

    row_num = 1
    while row_num <= num_rows:
        (
            customer_id,
            first_name,
            last_name,
            email,
            phone_number,
            registration_date_millis,
        ) = generate_random_data(row_num)

        customer_ids.append(customer_id)
        first_names.append(first_name)
        last_names.append(last_name)
        emails.append(email)
        phone_numbers.append(phone_number)
        registration_dates.append(registration_date_millis)
        row_num += 1

    df = pd.DataFrame(
        {
            "customer_id": customer_ids,
            "first_name": first_names,
            "last_name": last_names,
            "email": emails,
            "phone_number": phone_numbers,
            "registration_date": registration_dates,
        }
    )

    df.to_csv(output_file, index=False)

    print(f"{num_rows} rows of data generated and saved to {output_file}")


with DAG(
    "d_customer_generator",
    default_args=default_args,
    description="Generate large customer dimensions data in a CSV file",
    schedule_interval=timedelta(days=1),
    start_date=start_date,
    tags=["schema"],
) as dag:

    start = EmptyOperator(task_id="start_task")

    generate_customer_dim_data = PythonOperator(
        task_id="generate_customer_dim_data", python_callable=generate_customer_dim_data
    )

    end = EmptyOperator(task_id="end_task")

    start >> generate_customer_dim_data >> end
