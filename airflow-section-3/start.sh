#!/bin/bash

# Build the base images from which are based the Dockerfiles 
docker build -t hadoop-base docker/hadoop/hadoop-base
docker build -t hive-base docker/hive/hive-base
docker build -t spark-base docker/spark/spark-base

# Startup all the containers at once
docker-compose up -d --build
