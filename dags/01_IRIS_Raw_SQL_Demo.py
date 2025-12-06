from datetime import datetime
from airflow import DAG
from airflow_provider_iris.operators.iris_operator import IrisSQLOperator

with DAG(
    dag_id="01_IRIS_Raw_SQL_Demo",
    start_date=datetime(2025, 12, 1),
    schedule=None,
    catchup=False,
    tags=["iris-contest"],
) as dag:
    
    create_table = IrisSQLOperator(
        task_id="create_table",
        sql="""CREATE TABLE IF NOT EXISTS Test.AirflowDemo (
               ID INTEGER IDENTITY PRIMARY KEY,
               Message VARCHAR(200),
               RunDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
    )

    insert = IrisSQLOperator(
        task_id="insert_row",
        sql="INSERT INTO Test.AirflowDemo (Message) VALUES ('Hello from raw SQL operator')",
    )

    select = IrisSQLOperator(
        task_id="select_rows",
        sql="SELECT ID, Message, RunDate FROM Test.AirflowDemo ORDER BY ID DESC",
    )

    create_table >> insert >> select