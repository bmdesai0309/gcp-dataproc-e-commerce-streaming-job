import os
import sys
import pytest
from pyspark.sql import SparkSession
from src.common.schema import CLICKSTREAM_SCHEMA

@pytest.fixture(scope="session")
def spark():
    os.environ['PYSPARK_PYTHON'] = sys.executable
    os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
    return SparkSession.builder.master("local[1]").appName("UnitTests").getOrCreate()

def test_schema_application(spark):
    sample_json = '{"user_id": "123", "session_id": "abc", "event_type": "view", "event_timestamp": "2026-01-19T10:00:00Z"}'
    df = spark.read.json(spark.sparkContext.parallelize([sample_json]), schema=CLICKSTREAM_SCHEMA)
    assert df.count() == 1
    assert df.schema == CLICKSTREAM_SCHEMA