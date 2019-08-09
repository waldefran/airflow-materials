#!/usr/bin/env bash

# Create the user airflow in the HDFS
hdfs dfs -mkdir -p    /user/airflow/
hdfs dfs -chmod g+w   /user/airflow

# Move to the AIRFLOW HOME directory
cd $AIRFLOW_HOME

# Initiliase the metadatabase
airflow initdb

# Run the webserver in background and redirect the standard output and standard error to the file output.log
airflow webserver &> output.log &

# Run the scheduler
exec airflow scheduler