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
<img width="1528" alt="image" src="https://github.com/user-attachments/assets/63726129-57fd-4c0e-84b2-ef98b151c24f" />

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
Navigate to [http://localhost:8080/](http://localhost:8080/) to access the application [Credentials: airflow/airflow]
<img width="1528" alt="image" src="https://github.com/user-attachments/assets/e821d4b5-85a2-4ef6-a81f-bafa7e2aae5c" />


## View/Run Sample Dags
The application comes with three pre-loaded DAGs.
1. Open the Airflow UI and click on the **DAGs** tab.  
2. Use the toggle button next to each DAG to enable or disable it.
<img width="1533"  alt="image" src="https://github.com/user-attachments/assets/20773c69-9eca-40a8-b663-274598f6a545" />

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
[Credentials: _SYSTEM/SYS]
<img width="1784" alt="image" src="https://github.com/user-attachments/assets/f73553b2-ebdb-4e9d-b3ec-3ae196bf7921" />


### Add IRIS connection 
Go to Admin → Connections → Add Connection
<img width="1917" alt="image" src="https://github.com/user-attachments/assets/1dd6e368-0b63-45f9-9e00-b330bbcc8f41" />
Click on save button to add the connection
<img width="1127" alt="image" src="https://github.com/user-attachments/assets/7ba543e6-100b-49d5-88fb-1ed412f63d00" />

Use your InterSystems IRIS connection by setting the `iris_conn_id` parameter in any of the provided operators.

In the example below, the `IrisSQLOperator` uses the `iris_conn_id` parameter to connect to the IRIS instance when the DAG is defined: 
```python
#New_Test_DAG.py
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
Airflow automatically take the DAGS from DAG folder. add new python file in DAG folder. 
 
## About Airflow-provider-iris package
The Apache Airflow Provider for InterSystems IRIS enables Airflow users to connect to InterSystems IRIS databases and execute SQL tasks using a native Airflow connection type (iris).
### Installation
The **airflow-provider-iris** package can be installed separately in any Airflow environment using the following command:
```bash
pip install airflow-provider-iris
```
For detailed documentation, usage examples, and a complete list of operators/hooks, see the published provider package:
[![one](https://img.shields.io/badge/PyPI%20Package-airflow%20provider%20iris-yellowgreen)](https://pypi.org/project/airflow-provider-iris/)
<img width="1609" height="977" alt="image" src="https://github.com/user-attachments/assets/2ead3589-2f28-4b50-a54a-45e45cbb4e1a" />
