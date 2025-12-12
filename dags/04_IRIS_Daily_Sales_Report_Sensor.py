# dags/04_IRIS_Daily_Sales_Report_Sensor.py
#
# Example DAG that shows the full power of the airflow-provider-iris package:
#   • IrisSensor  – waits until the daily bulk load has finished
#   • IrisSQLOperator – creates table + truncates + inserts summary data
#
# This DAG depends on the bulk-load DAG (03_IRIS_Load_Synthetic_Data_Demo)
# which populates AirflowDemo.BulkSales with ~200 synthetic rows per day.

from datetime import datetime
from airflow import DAG

# Provider classes – install with: pip install airflow-provider-iris
from airflow_provider_iris.sensors.iris_sensor import IrisSensor
from airflow_provider_iris.operators.iris_sql_operator import IrisSQLOperator


with DAG(
    dag_id="04_IRIS_Daily_Sales_Report_Sensor",
    schedule="0 5 * * *",                 # Run every day at 05:00 AM (after bulk load expected)
    start_date=datetime(2025, 12, 1),
    catchup=False,                         # Don't backfill historic dates
    tags=["iris", "sales", "demo", "reporting"],
    doc_md=__doc__,                        # Shows this header comment in the UI
) as dag:

    # ------------------------------------------------------------------
    # 1. Wait until today's bulk load has delivered enough rows
    # ------------------------------------------------------------------
    wait_for_bulk_load = IrisSensor(
        task_id="wait_for_today_bulk_load",
        sql="""
            SELECT COUNT(*) 
            FROM AirflowDemo.BulkSales 
            WHERE CAST(entry_date AS DATE) = '{{ ds }}'
        """,
        expected_result=200,      # We normally get ~200 rows from the bulk load
        tolerance=80,             # Accept anything from ~120 upwards
        poke_interval=60,         # Check every minute
        timeout=6 * 3600,         # Give up after 6 hours if data never arrives
        mode="reschedule",        # Free the worker slot while waiting
    )

    # ------------------------------------------------------------------
    # 2. Make sure the summary table exists (idempotent – safe to run every day)
    # ------------------------------------------------------------------
    create_summary_table = IrisSQLOperator(
        task_id="create_summary_table_if_not_exists",
        sql="""
            CREATE TABLE IF NOT EXISTS AirflowDemo.RegionalSummary (
                ReportDate     DATE,
                Region         VARCHAR(50),
                Transactions   INTEGER,
                TotalRevenue   DECIMAL(16,2),
                AvgDealSize    DECIMAL(16,2)
            )
        """,
    )

    # ------------------------------------------------------------------
    # 3. Remove any previous summary for today (in case we re-run the DAG)
    # ------------------------------------------------------------------
    truncate_today = IrisSQLOperator(
        task_id="truncate_today_data",
        sql="""
            DELETE FROM AirflowDemo.RegionalSummary 
            WHERE ReportDate = TO_DATE('{{ ds }}', 'YYYY-MM-DD')
        """,
    )

    # ------------------------------------------------------------------
    # 4. Build the regional sales summary for the execution date
    #    TO_DATE() is required – IRIS does not implicitly convert 'YYYY-MM-DD' strings to DATE
    # ------------------------------------------------------------------
    insert_today_summary = IrisSQLOperator(
        task_id="insert_today_regional_summary",
        sql="""
            INSERT INTO AirflowDemo.RegionalSummary
            SELECT 
                TO_DATE('{{ ds }}', 'YYYY-MM-DD') AS ReportDate,
                region,
                COUNT(*)                  AS Transactions,
                SUM(amount)               AS TotalRevenue,
                AVG(amount)               AS AvgDealSize
            FROM AirflowDemo.BulkSales
            WHERE CAST(entry_date AS DATE) = '{{ ds }}'
            GROUP BY region
        """,
    )

    # ------------------------------------------------------------------
    # Task dependencies – Airflow executes in this exact order
    # ------------------------------------------------------------------
    (
        wait_for_bulk_load
        >> create_summary_table
        >> truncate_today
        >> insert_today_summary
    )