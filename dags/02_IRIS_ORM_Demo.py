# dags/02_IRIS_ORM_Demo.py

from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import numpy as np

# Import IRIS hook and SQLAlchemy components
from airflow_provider_iris.hooks.iris_hook import IrisHook
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# ---------------------------------------------------------------------
# ORM MODEL
# Defines the structure of the AirflowDemo.ORMSales table in IRIS.
# ---------------------------------------------------------------------
class SalesRecord(Base):
    __tablename__ = "ORMSales"
    __table_args__ = {"schema": "AirflowDemo"}

    id        = Column(Integer, primary_key=True)
    region    = Column(String(50))
    amount    = Column(Float)
    sale_date = Column(DateTime)


# ---------------------------------------------------------------------
# TASK 1: Create table and insert synthetic sample records.
# Uses pandas.to_sql() with chunksize=1 → most consistent for IRIS.
# ---------------------------------------------------------------------
def create_and_insert_orm(**context):
    # If you use a non-default connection → ALWAYS pass iris_conn_id explicitly
    # e.g hook = IrisHook(iris_conn_id="iris_Connection_ID")
    hook = IrisHook()
    engine = hook.get_engine()

    # Ensure the table exists
    Base.metadata.create_all(engine)

    # ---- Generate synthetic generic sample data ----
    num_records = 5
    regions = [f"Region {i}" for i in range(1, num_records + 1)]

    sample_data = [
        {
            "region": region,
            "amount": round(np.random.uniform(5000, 50000), 2),
            "sale_date": pd.Timestamp("2025-12-01") + pd.Timedelta(days=i)
        }
        for i, region in enumerate(regions)
    ]

    df = pd.DataFrame(sample_data)

    # Insert rows → IRIS requires single-batch inserts for reliability
    df.to_sql(
        name="ORMSales",
        con=engine,
        schema="AirflowDemo",
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1,   # key setting for IRIS compatibility
    )

    print(f"Inserted {len(df)} generated rows into AirflowDemo.ORMSales")


# ---------------------------------------------------------------------
# TASK 2: Query back data and print rows in Airflow logs.
# ---------------------------------------------------------------------
def query_orm(**context):
    hook = IrisHook()
    engine = hook.get_engine()

    df = pd.read_sql(
        "SELECT * FROM AirflowDemo.ORMSales ORDER BY id",
        engine
    )

    for _, r in df.iterrows():
        print(
            f"ORM → {int(r.id):>3} | "
            f"{r.region:<15} | "
            f"${r.amount:>10,.2f} | "
            f"{r.sale_date.date()}"
        )


# ---------------------------------------------------------------------
# DAG DEFINITION
# ---------------------------------------------------------------------
with DAG(
    dag_id="02_IRIS_ORM_Demo",
    start_date=datetime(2025, 12, 1),
    schedule=None,
    catchup=False,
    tags=["iris-contest", "orm"],
) as dag:

    orm_create = PythonOperator(
        task_id="orm_create_and_insert",
        python_callable=create_and_insert_orm,
    )

    orm_read = PythonOperator(
        task_id="orm_read",
        python_callable=query_orm,
    )

    orm_create >> orm_read
