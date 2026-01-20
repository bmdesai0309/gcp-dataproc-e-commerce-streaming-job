#!/usr/bin/env bash

export PYSPARK_PYTHON=python

PROJECT_ROOT=$(pwd)
JAR_PATH="${PROJECT_ROOT}/jars/custom-udf/target/custom-udf-1.0.jar"
PYTHON_JOB="${PROJECT_ROOT}/src/jobs/kafka_to_bq.py"

if [ ! -f "${JAR_PATH}" ]; then
  echo "Building JAVA UDF JAR... "
  cd jars/custom-udf && mvn clean package && cd ../..
fi

#
# spark-submit \
#  --master local[*] \
#  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 \
#  --jars "${JAR_PATH}" \
#  --py-files "${PYTHON_JOB}" \
#  "$PYTHON_JOB"

python src/jobs/kafka_to_bq.py