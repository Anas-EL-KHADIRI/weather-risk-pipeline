FROM apache/airflow:2.9.3 
COPY ./requirements.txt .


RUN pip install -r requirements.txt
COPY ./dags/weather_pipeline.py /opt/airflow/dags

COPY extraction/ /opt/airflow/extraction/
COPY transformation/ /opt/airflow/transformation/
COPY load/ /opt/airflow/load/

COPY bronze/ /opt/airflow/bronze/
COPY silver/ /opt/airflow/silver/
COPY gold/ /opt/airflow/gold/

COPY .env /opt/airflow/.env

USER root

RUN chown -R airflow:root /opt/airflow/bronze /opt/airflow/silver /opt/airflow/gold

USER airflow

ENV PYTHONPATH=/opt/airflow