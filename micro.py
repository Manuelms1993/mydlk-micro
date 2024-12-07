from fastapi import FastAPI, HTTPException
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from typing import Dict
import logging

# logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# API
app = FastAPI()

spark = SparkSession.builder \
    .appName("API") \
    .config("spark.sql.warehouse.dir", "hdfs://namenode:9000/user/hive/warehouse") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
    .config("spark.hadoop.hive.metastore.uris", "thrift://hive-metastore:9083") \
    .config("dfs.datanode.use.datanode.hostname", "true") \
    .config("dfs.client.use.datanode.hostname", "true") \
    .enableHiveSupport() \
    .getOrCreate()


# Function to fetch a row from Hive using PySpark
def fetch_row_from_hive(row_id: str = None, name: str = None) -> Dict:
    try:
        df = spark.sql(f"SELECT * FROM bi.films_imdb")

        if name is None:
            result = df.filter(col("id") == row_id).collect()
        else:
            result = df.filter(col("title") == name).collect()

        logger.info(f"OK")

        if not result:
            raise HTTPException(status_code=404, detail="Row not found")

        # Convert the result to a dictionary (assumes single result for unique ID)
        return {field: value for field, value in zip(result[0].__fields__, result[0])}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying Hive: {str(e)}")


# FastAPI GET endpoint
@app.get("/get-imdb-film/")
def get_row(id: str):
    """
    Retrieve a row from a Hive table based on row ID using PySpark.
    """
    return fetch_row_from_hive(row_id=id)

@app.get("/get-imdb-film-by-name/")
def get_row(name: str):
    """
    Retrieve a row from a Hive table based on name
    """
    return fetch_row_from_hive(name=name)