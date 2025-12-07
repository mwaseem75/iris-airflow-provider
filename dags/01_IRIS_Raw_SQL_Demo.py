from datetime import datetime
from airflow import DAG
from airflow_provider_iris.operators.iris_operator import IrisSQLOperator

# ---------------------------------------------------------------------
# Example DAG showing how to run raw SQL statements on InterSystems IRIS
# using the IrisSQLOperator included in the provider.
# ---------------------------------------------------------------------

with DAG(
    dag_id="01_IRIS_Raw_SQL_Demo",
    start_date=datetime(2025, 12, 1),
    schedule=None,        # Run manually – no recurring schedule
    catchup=False,
    tags=["iris-contest"],
) as dag:
    
    # Create a simple table to store demo entries.
    # IF NOT EXISTS ensures the DAG can be re-run without errors.
    create_table = IrisSQLOperator(
        task_id="create_table",
        sql="""
            CREATE TABLE IF NOT EXISTS AirflowDemo.Test (
                ID INTEGER IDENTITY PRIMARY KEY,
                Message VARCHAR(200),
                RunDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """,
    )

    # Insert a sample row into the table.
    # This demonstrates a basic INSERT operation using the operator.
    insert = IrisSQLOperator(
        task_id="insert_row",
        sql="""
            INSERT INTO AirflowDemo.Test (Message)
            VALUES ('Hello from raw SQL operator')
        """,
    )

    # Retrieve all rows so the results appear in the Airflow logs.
    # Useful to confirm end-to-end connectivity with IRIS.
    select = IrisSQLOperator(
        task_id="select_rows",
        sql="""
            SELECT ID, Message, RunDate
            FROM AirflowDemo.Test
            ORDER BY ID DESC
        """,
    )

    # Task order: create table → insert row → select rows
    create_table >> insert >> select
