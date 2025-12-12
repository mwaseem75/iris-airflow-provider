from datetime import datetime
from airflow import DAG
from airflow_provider_iris.operators.iris_operator import IrisSQLOperator
#Define the DAG for running a simple SQL command against InterSystems IRIS.
with DAG(
dag_id="04_IRIS_TEST_DAG",
start_date=datetime(2025, 12, 1),
schedule=None,               # Run manually; no automatic scheduling
catchup=False,               # Do not backfill previous dates
tags=["iris-contest"],       # Tag to group the DAG in Airflow UI
) as dag:
# Create a demo table if it does not already exist.
# This operator connects to the specified IRIS instance and executes the SQL.
    create_table = IrisSQLOperator(
        task_id="create_table",
        iris_conn_id="ContainerInstance",   # Airflow connection configured for IRIS
        sql="""
            CREATE TABLE IF NOT EXISTS Test.AirflowDemo (
                ID INTEGER IDENTITY PRIMARY KEY,
                Message VARCHAR(200),
                RunDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)