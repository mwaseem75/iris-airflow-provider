# dags/example_synthetic_sales_dag.py

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import numpy as np
from airflow_provider_iris.hooks.iris_hook import IrisHook
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# ---------------------------------------------------------------------
# ORM model representing a generic sales table in the "AirflowDemo" schema.
# Reusable for both table creation and data insertion.
# ---------------------------------------------------------------------
class SalesRecord(Base):
    __tablename__ = "BulkSales"
    __table_args__ = {"schema": "AirflowDemo"}

    id        = Column(Integer, primary_key=True)
    region    = Column(String(50))
    amount    = Column(Float)
    sale_date = Column(DateTime)
    entry_date = Column(DateTime, default=datetime.now)


# ---------------------------------------------------------------------
# Generate synthetic sales data for testing or demo purposes.
# Supports dynamic number of rows and produces realistic random data.
# ---------------------------------------------------------------------
def generate_synthetic_sales(num_rows=200):
    regions = ["North America", "South America", "Europe", "Asia-Pacific", "Middle East", "Africa"]

    region_data = np.random.choice(regions, size=num_rows)
    amounts = np.random.uniform(10000, 120000, size=num_rows).round(2)

    # Random business dates in last 60 days
    start_date = datetime.now() - timedelta(days=60)
    sale_dates = [start_date + timedelta(days=np.random.randint(0, 61)) for _ in range(num_rows)]

    df = pd.DataFrame({
        "region": region_data,
        "amount": amounts,
        "sale_date": sale_dates,
        "entry_date": pd.Timestamp.utcnow()   # ← Perfect: one value, auto-broadcast, UTC
    })

    return df
    

# ---------------------------------------------------------------------
# Airflow task: bulk load synthetic sales data into IRIS.
# ---------------------------------------------------------------------
def bulk_load_synthetic_sales(**context):

    # Generate synthetic dataset
    df = generate_synthetic_sales(num_rows=200)

    # Create SQLAlchemy engine via IRIS hook
    # If you use a non-default connection → ALWAYS pass iris_conn_id explicitly
    # e.g hook = IrisHook(iris_conn_id="iris_Connection_ID")
    hook = IrisHook()
    engine = hook.get_engine()

    # Ensure table exists
    Base.metadata.create_all(engine)

    # Bulk insert into IRIS
    df.to_sql(
        "BulkSales",
        con=engine,
        schema="AirflowDemo",
        if_exists="append",
        index=False
    )

    print(f"Bulk loaded {len(df)} synthetic rows into AirflowDemo.BulkSales")


# ---------------------------------------------------------------------
# DAG definition
# Demonstrates ETL-style bulk load of synthetic sales data into IRIS.
# ---------------------------------------------------------------------
with DAG(
    dag_id="03_IRIS_Load_Synthetic_Data_Demo",
    start_date=datetime(2025, 12, 1),
    schedule=None,
    catchup=False,
    tags=["iris-contest", "etl", "synthetic"],
) as dag:

    bulk_task = PythonOperator(
        task_id="bulk_load_synthetic_sales",
        python_callable=bulk_load_synthetic_sales
    )
