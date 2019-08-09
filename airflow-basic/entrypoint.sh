#!/usr/bin/env bash

# Initiliase the metadatabase
airflow initdb

# Run the webserver in background and redirect the standard output and standard error to the file output.log
airflow webserver &> output.log &

# Run the scheduler
exec airflow scheduler