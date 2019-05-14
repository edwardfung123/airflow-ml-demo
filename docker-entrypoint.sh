#!/usr/bin/env bash

set -e

airflow initdb
airflow webserver -p 8080
