<h1>Intersystems IRIS provider for Apache Airflow</h1>
<img width="630" alt="image" src="https://raw.githubusercontent.com/mwaseem75/airflow-provider-iris/main/images/airflowlogo.png" />

[![PyPI version](https://badge.fury.io/py/airflow-provider-iris.svg)](https://badge.fury.io/py/airflow-provider-iris)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/airflow-provider-iris)](https://pypistats.org/packages/airflow-provider-iris)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Contest Entry](https://img.shields.io/badge/InterSystems-Developer%20Contest%202025-FF6A00.svg)](https://openexchange.intersystems.com/contest/current)
#### Production-ready integration between Apache Airflow and InterSystems IRIS Data Platform.
<img width="1918" alt="image" src="https://raw.githubusercontent.com/mwaseem75/airflow-provider-iris/main/images/mainscreenshot.png" />

Seamlessly orchestrate InterSystems IRIS workloads from Apache Airflow:
- Native SQL execution with full templating support
- Reliable bulk data loading via SQLAlchemy + pandas
- Full connection management with Airflow Connections
- Built for production ETL, analytics, and healthcare workflows

---

### Features

- `IrisSQLOperator` – Execute raw SQL/ObjectScript with Jinja templating
- `IrisHook` – SQLAlchemy-compatible hook for pandas, ORM, and custom logic
- Full support for IRIS namespaces, schemas, and authentication
- Works reliably with `pandas.to_sql()` (critical fix: `chunksize=1` for IRIS compatibility)
- Zero external dependencies beyond standard Airflow & IRIS Python drivers
- Comprehensive examples for real-world ETL patterns

---

### Installation

```bash
pip install airflow-provider-iris
```
### Quick Start (Create IRIS connection)

Configure Connection in Airflow UI
Go to Admin → Connections → Add Connection
<img width="1127" alt="image" src="https://raw.githubusercontent.com/mwaseem75/airflow-provider-iris/main/images/connection.png" />

Use your InterSystems IRIS connection by setting the `iris_conn_id` parameter in any of the provided operators.

In the example below, the `IrisSQLOperator` uses the `iris_conn_id` parameter to connect to the IRIS instance when the DAG is defined: 
```python
from airflow_provider_iris.operators.iris_operator import IrisSQLOperator

with DAG(
    dag_id="01_IRIS_Raw_SQL_Demo_Local",
    start_date=datetime(2025, 12, 1),
    schedule=None,
    catchup=False,
    tags=["iris-contest"],
) as dag:
    
    create_table = IrisSQLOperator(
        task_id="create_table",
        iris_conn_id="ContainerInstance",
        sql="""CREATE TABLE IF NOT EXISTS Test.AirflowDemo (
               ID INTEGER IDENTITY PRIMARY KEY,
               Message VARCHAR(200),
               RunDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
    )
```
### Example DAGs (Included in examples/)
1. Raw SQL Operator – Simple & Powerful
```python
# dags/01_IRIS_Raw_SQL_Demo.py
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
```

2. ORM + Pandas Integration (Real-World ETL)
Uses SQLAlchemy + pandas with the only known reliable method for bulk inserts into IRIS.
```
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
```
3. Synthetic Data Generator → Bulk Load
Generate realistic sales data and load efficiently.

```
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

```


    
