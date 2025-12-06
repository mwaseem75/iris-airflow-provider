FROM apache/airflow:3.1.3

COPY requirements.txt /requirements.txt

RUN pip install  --upgrade pip

RUN pip install --no-cache-dir -r /requirements.txt

# WORKDIR /app
# # Copy your wheel file
# COPY airflow_provider_iris-0.0.0+develop-py3-none-any.whl /app/

# RUN pip install --no-cache-dir airflow_provider_iris-0.0.0+develop-py3-none-any.whl

