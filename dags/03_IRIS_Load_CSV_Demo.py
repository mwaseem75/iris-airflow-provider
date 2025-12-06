from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import numpy as np
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


# ----------- SYNTHETIC DATA GENERATION -----------
def generate_synthetic_sales(num_rows=500):
    """Create synthetic sales data for testing."""
    
    regions = [
        "North America", "South America", "Europe",
        "Asia-Pacific", "Middle East", "Africa"
    ]

    # Randomly pick regions
    region_data = np.random.choice(regions, size=num_rows)

    # Generate synthetic amounts between 10k and 120k
    amounts = np.random.uniform(10000, 120000, size=num_rows).round(2)

    # Generate random dates within last 30 days
    start_date = datetime(2025, 11, 1)
    sale_dates = [start_date + timedelta(days=int(x)) for x in np.random.randint(0, 30, size=num_rows)]

    df = pd.DataFrame({
        "region": region_data,
        "amount": amounts,
        "sale_date": sale_dates
    })

    return df


# ----------- AIRFLOW TASK FUNCTION -----------
def bulk_load_from_csv(**context):

    df = generate_synthetic_sales(num_rows=200)   # Change number as needed

    hook = IrisHook()
    engine = hook.get_engine()

    Base.metadata.create_all(engine)

    df.to_sql("SalesRecord", con=engine, schema="Test", if_exists="append", index=False)
    print(f"Bulk loaded {len(df)} synthetic rows via pandas.to_sql()")


# ----------- DAG DEFINITION -----------
with DAG(
    dag_id="03_IRIS_Load_CSV_Synthetic_Demo",
    start_date=datetime(2025, 12, 1),
    schedule=None,
    catchup=False,
    tags=["iris-contest", "etl", "synthetic"],
) as dag:

    bulk_task = PythonOperator(
        task_id="bulk_load_synthetic_to_iris",
        python_callable=bulk_load_from_csv
    )
