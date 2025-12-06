# dags/example_sqlalchemy_dag.py

from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd

# Import your hook and model
from airflow_provider_iris.hooks.iris_hook import IrisHook
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class SalesRecord(Base):
    __tablename__ = "SalesRecord"
    __table_args__ = {"schema": "Test"}

    id        = Column(Integer, primary_key=True)
    region    = Column(String(50))
    amount    = Column(Float)
    sale_date = Column(DateTime)

def create_and_insert_orm(**context):
    hook = IrisHook()
    engine = hook.get_engine()

    # Create table if not exists
    Base.metadata.create_all(engine)

    # THIS IS THE ONLY METHOD THAT WORKS RELIABLY WITH IRIS RIGHT NOW
    data = [
        {"region": "Europe",        "amount": 12500.50, "sale_date": "2025-12-01"},
        {"region": "Asia",          "amount": 8900.00,  "sale_date": "2025-12-02"},
        {"region": "North America", "amount": 56700.00, "sale_date": "2025-12-03"},
        {"region": "Africa",        "amount": 34200.00, "sale_date": "2025-12-03"},
    ]
    df = pd.DataFrame(data)
    df["sale_date"] = pd.to_datetime(df["sale_date"])

    # pandas.to_sql with single-row inserts → IRIS accepts this perfectly
    df.to_sql(
        name="SalesRecord",
        con=engine,
        schema="Test",
        if_exists="append",
        index=False,
        method="multi",           # still fast
        chunksize=1               # ← THIS IS THE MAGIC LINE
    )
    print(f"Successfully inserted {len(df)} rows using pandas.to_sql() (chunksize=1)")


def query_orm(**context):
    hook = IrisHook()
    engine = hook.get_engine()
    df = pd.read_sql("SELECT * FROM Test.SalesRecord ORDER BY id", engine)
    for _, r in df.iterrows():
        print(f"ORM → {int(r.id):>3} | {r.region:<15} | ${r.amount:>10,.2f} | {r.sale_date.date()}")


with DAG(
    dag_id="02_IRIS_ORM_Demo",
    start_date=datetime(2025, 12, 1),
    schedule=None,
    catchup=False,
    tags=["iris-contest", "orm"],
) as dag:

    orm_create = PythonOperator(task_id="orm_create_and_insert", python_callable=create_and_insert_orm)
    orm_read   = PythonOperator(task_id="orm_read",               python_callable=query_orm)

    orm_create >> orm_read