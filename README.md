<h1>Intersystems IRIS provider for Apache Airflow</h1>
<img width="530" alt="image" src="https://github.com/user-attachments/assets/99d107ab-69d0-4e89-a51a-cf78867d618e" />

[![one](https://img.shields.io/badge/Platform-InterSystems%20IRIS-blue)](https://www.intersystems.com/data-platform/)
[![one](https://img.shields.io/badge/Workflow%20Orchestration-Aoache%20Airflow-success)](https://airflow.apache.org/)
[![one](https://img.shields.io/badge/PyPI%20Package-airflow%20provider%20iris-yellowgreen)](https://pypi.org/project/airflow-provider-iris/)
[![one](https://img.shields.io/badge/PyPI%20Availabe%20on-Open%20Exchange-blue)](https:///)
[![License](https://img.shields.io/badge/License-Apache%202.0-00b2a9.svg)](https://opensource.org/licenses/Apache-2.0)
The InterSystems IRIS Provider for Apache Airflow enables seamless integration between Airflow workflows and the InterSystems IRIS data platform. It provides native connection support and operators for executing IRIS SQL and automating IRIS-driven tasks within modern ETL/ELT pipelines.

Designed for reliability and ease of use, this provider helps data engineers and developers build scalable, production-ready workflows for healthcare, interoperability, analytics, and enterprise data processing—powered by InterSystems IRIS.

## About Apache Airflow
[Apache Airflow](https://airflow.apache.org/) is the leading open-source platform to programmatically author, schedule, and monitor data pipelines and workflows using Python. Workflows are defined as code (DAGs), making them version-controlled, testable, and reusable. With a rich UI, 100+ built-in operators, dynamic task generation, and native support for cloud providers, Airflow powers ETL/ELT, ML pipelines, and batch jobs at companies like Airbnb, Netflix, and Spotify.

### Application Layout
<img width="1528" height="780" alt="image" src="https://github.com/user-attachments/assets/63726129-57fd-4c0e-84b2-ef98b151c24f" />

### Provider Features
* ✔️ `IrisHook` – for managing IRIS connections
* ✔️ `IrisSQLOperator` – for running SQL queries
* ✔️ Support for both SELECT/CTE and DML statements
* ✔️ Native Airflow connection UI customization
* ✔️ Examples for real-world ETL patterns

---

## Installation 

### Docker (e.g. for dev purposes)

Clone/git pull the repo into any local directory

```
$ git clone https://github.com/mwaseem75/iris-airflow-provider.git
```
Open the terminal in this directory and run below commands:

Initializes the Airflow metadata database

```
$ docker compose up airflow-init
```
Initializes IRIS and entire Airflow platform
```
$ docker-compose up -d
```

## Run the Application
Navigate to [http://localhost:8080/](http://localhost:8080/) to access the application.
<img width="1528" height="780" alt="image" src="https://github.com/user-attachments/assets/e821d4b5-85a2-4ef6-a81f-bafa7e2aae5c" />


## View/Run Sample Dags
The application comes with three pre-loaded DAGs.
1. Open the Airflow UI and click on the **DAGs** tab.  
2. Use the toggle button next to each DAG to enable or disable it.
<img width="1533" height="748" alt="image" src="https://github.com/user-attachments/assets/20773c69-9eca-40a8-b663-274598f6a545" />

To run a DAG manually, click the **Trigger DAG** button (▶ arrow) on the right side of the DAG row.
Click the name of DAG (e.g., **01_IRIS_Raw_SQL_Demo**) to view its details, graph, and run history.
<img width="1915"  alt="image" src="https://github.com/user-attachments/assets/4418ffff-667a-4721-96b6-89f8b3f84736" />
The **01_IRIS_Raw_SQL_Demo** DAG consists of three tasks:
1. Create Table
2. Insert Data
3. Retrieve Data
<img width="1918" alt="image" src="https://github.com/user-attachments/assets/14bead69-2a4d-4ca8-b723-0550433f4e5b" />
Select a task and click the task box to open its details.
Click **Details** tab to see its details.

<img width="1913" alt="image" src="https://github.com/user-attachments/assets/176ea66e-857c-4089-b91a-f0f9442b36e4" />
Click **Code** tab to see the task’s source code.
<img width="1896" alt="image" src="https://github.com/user-attachments/assets/1125ad52-c1da-4232-af52-6a7dfd1567fb" />
Then click **Log** tab to see the Log details.
<img width="1917" alt="image" src="https://github.com/user-attachments/assets/ecc71e50-038c-4439-b503-639ac502fdfe" />
If the DAG runs successfully, verify the results in the InterSystems Management Portal. 
Navigate to http://localhost:32783/csp/sys/exp/%25CSP.UI.Portal.SQL.Home.zen?$NAMESPACE=USER
[Credentials: _SYSTEM/`SYS`]
<img width="1529" height="708" alt="image" src="https://github.com/user-attachments/assets/942fe4a1-19cc-4974-ab99-21c06d72e0c7" />

## About Airflow-provider-iris package
The Apache Airflow Provider for InterSystems IRIS enables Airflow users to connect to InterSystems IRIS databases and execute SQL tasks using a native Airflow connection type (iris).
### Installation
The **airflow-provider-iris** package can be installed separately in any Airflow environment using the following command:
```bash
pip install airflow-provider-iris
```
For more details, visit the package on PyPI: 
[![one](https://img.shields.io/badge/PyPI%20Package-airflow%20provider%20iris-yellowgreen)](https://pypi.org/project/airflow-provider-iris/)
<img width="1563" alt="image" src="https://github.com/user-attachments/assets/c28036a4-30b6-4031-ac47-e4f030071a48" />

### Add IRIS connection 
Go to Admin → Connections → Add Connection
<img width="1917" alt="image" src="https://github.com/user-attachments/assets/1dd6e368-0b63-45f9-9e00-b330bbcc8f41" />
Click on save button to add the connection
<img width="1127" alt="image" src="https://github.com/user-attachments/assets/7ba543e6-100b-49d5-88fb-1ed412f63d00" />

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


## ADD new DAG
**DAG** (Directed Acyclic Graph) – a Python script that defines a workflow as a collection of tasks with dependencies and schedule in Apache Airflow.
Airflow automatically take the DAGS from DAG folder. add new python file in DAG folder:

Click on Create table task then click on 



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


    
