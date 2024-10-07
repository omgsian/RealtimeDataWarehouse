from airflow import DAG
import pandas as pd
from datetime import datetime, timedelta
import random
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

start_date = datetime(2024, 9, 15)
default_args = {"owner": "mrh", "depends_on_past": False, "backfill": False}

num_rows = 50
output_file = "./branch_dim_large_data.csv"

cities = [
    "New York, New York",
    "Los Angeles, California",
    "Chicago, Illinois",
    "Houston, Texas",
    "Phoenix, Arizona",
    "Philadelphia, Pennsylvania",
]

regions = [
    "California",
    "Texas",
    "Florida",
    "New York",
    "Pennsylvania",
    "Illinois",
]

postcodes = [
    "90210",
    "10001",
    "77002",
    "60611",
    "19103",
    "85004",
]


def generate_random_data(row_num):
    branch_id = f"B{row_num:05d}"
    branch_name = f"Branch {row_num}"
    branch_address = f'{random.randint(1,999)} {random.choice(["Main St", "Park Ave", "Oak St", "Maple Ave", "Elm St"])}'
    city = random.choice(cities)
    region = random.choice(regions)
    postcode = random.choice(postcodes)

    now = datetime.now()
    random_date = now - timedelta(days=random.randint(0, 3650))
    opening_date_millis = int(random_date.timestamp() * 1000)

    return (
        branch_id,
        branch_name,
        branch_address,
        city,
        region,
        postcode,
        opening_date_millis,
    )


branch_ids = []
branch_names = []
branch_addresses = []
cities_ls = []
regions_ls = []
postcodes_ls = []
opening_dates = []


def generate_branch_dim_data():
    row_num = 1
    while row_num <= num_rows:
        data = generate_random_data(row_num)
        print(data)
        branch_ids.append(data[0])
        branch_names.append(data[1])
        branch_addresses.append(data[2])
        cities_ls.append(data[3])
        regions_ls.append(data[4])
        postcodes_ls.append(data[5])
        opening_dates.append(data[6])
        row_num += 1

    df = pd.DataFrame(
        {
            "branch_id": branch_ids,
            "branch_name": branch_names,
            "branch_address": branch_addresses,
            "city": cities_ls,
            "state": regions_ls,
            "zipcode": postcodes_ls,  # Note: changed from 'postcode' to 'zipcode'
        }
    )

    df.to_csv(output_file, index=False)

    print(f"{num_rows} rows of data generated and saved to {output_file}")


with DAG(
    "d_branch_generator",
    default_args=default_args,
    description="Generate large branch dimensions data in a CSV file",
    schedule_interval=timedelta(days=1),
    start_date=start_date,
    tags=["schema"],
) as dag:

    start = EmptyOperator(task_id="start_task")

    generate_branch_dim_data = PythonOperator(
        task_id="generate_branch_dim_data", python_callable=generate_branch_dim_data
    )

    end = EmptyOperator(task_id="end_task")

    start >> generate_branch_dim_data >> end
