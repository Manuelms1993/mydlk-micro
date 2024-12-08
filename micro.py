from fastapi import FastAPI, HTTPException
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from typing import Dict
import logging

from sqlalchemy.util import deprecated

from schemas import FilmEntry, schemaFilmEntry

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


@app.post("/create-film/")
def create_film(entry: FilmEntry):
    try:
        data = [(
            entry.id, entry.title, entry.type, entry.release_year,
            entry.age_certification, entry.runtime, entry.genres,
            entry.production_countries, entry.seasons, entry.imdb_score,
            entry.imdb_votes, entry.tmdb_popularity, entry.tmdb_score
        )]

        columns = [
            "id", "title", "type", "release_year", "age_certification",
            "runtime", "genres", "production_countries", "seasons",
            "imdb_score", "imdb_votes", "tmdb_popularity", "tmdb_score"
        ]

        df = spark.createDataFrame(data, schema=columns)
        df.write.mode("append").insertInto("bi.films_imdb")
        return {"status": "success", "message": "Film entry created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to insert into Hive: {str(e)}")

@app.put("/insert-if-not-exist-film/")
def upsert_film(entry: FilmEntry):
    try:
        # Check if the record already exists
        existing_records = spark.sql(
            f"SELECT * FROM bi.films_imdb WHERE id = '{entry.id}'"
        )
        if not existing_records.isEmpty():
            return {
                "status": "fail",
                "message": f"Record with ID '{entry.id}' already exists."
            }

        data = [(
            entry.id, entry.title, entry.type, entry.release_year,
            entry.age_certification, entry.runtime, entry.genres,
            entry.production_countries, entry.seasons, entry.imdb_score,
            entry.imdb_votes, entry.tmdb_popularity, entry.tmdb_score
        )]

        columns = [
            "id", "title", "type", "release_year", "age_certification",
            "runtime", "genres", "production_countries", "seasons",
            "imdb_score", "imdb_votes", "tmdb_popularity", "tmdb_score"
        ]

        df = spark.createDataFrame(data, schema=columns)
        df.write.mode("append").insertInto("bi.films_imdb")
        return {"status": "success", "message": "Film entry inserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to insert into Hive: {str(e)}")

@deprecated # only testing purpose (inefficient)
@app.patch("/update-film/{film_id}")
def update_film(film_id: str, entry: FilmEntry):
    try:
        existing_records = spark.sql(
            f"SELECT * FROM bi.films_imdb WHERE id = '{film_id}'"
        )

        if existing_records.count() == 0:
            raise HTTPException(status_code=404, detail=f"Film with ID {film_id} not found.")

        existing_data = existing_records.collect()[0].asDict()

        if entry.title is not None:
            existing_data["title"] = entry.title
        if entry.type is not None:
            existing_data["type"] = entry.type
        if entry.release_year is not None:
            existing_data["release_year"] = entry.release_year
        if entry.age_certification is not None:
            existing_data["age_certification"] = entry.age_certification
        if entry.runtime is not None:
            existing_data["runtime"] = entry.runtime
        if entry.genres is not None:
            existing_data["genres"] = entry.genres
        if entry.production_countries is not None:
            existing_data["production_countries"] = entry.production_countries
        if entry.seasons is not None:
            existing_data["seasons"] = entry.seasons
        if entry.imdb_score is not None:
            existing_data["imdb_score"] = entry.imdb_score
        if entry.imdb_votes is not None:
            existing_data["imdb_votes"] = entry.imdb_votes
        if entry.tmdb_popularity is not None:
            existing_data["tmdb_popularity"] = entry.tmdb_popularity
        if entry.tmdb_score is not None:
            existing_data["tmdb_score"] = entry.tmdb_score

        updated_df = spark.createDataFrame([existing_data], schema=schemaFilmEntry)
        updated_table_df = spark.sql(f"SELECT * FROM bi.films_imdb WHERE id != '{film_id}'")
        final_df = updated_table_df.union(updated_df)
        final_df.write.mode("overwrite").insertInto("bi.films_imdb")

        return {"status": "success", "message": f"Film {film_id} updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update film: {str(e)}")

@app.delete("/delete-film/{film_id}")
def delete_film(film_id: str):
    try:
        # Step 1: Check if the film exists in the table
        existing_records = spark.sql(
            f"SELECT * FROM bi.films_imdb WHERE id = '{film_id}'"
        )

        if existing_records.count() == 0:
            raise HTTPException(status_code=404, detail=f"Film with ID {film_id} not found.")

        # Step 2: Overwrite the table with all records except the one we want to delete
        # Using INSERT OVERWRITE to effectively delete the row
        spark.sql(f"""
            INSERT OVERWRITE TABLE bi.films_imdb
            SELECT * FROM bi.films_imdb
            WHERE id != '{film_id}'
        """)

        return {"status": "success", "message": f"Film {film_id} deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete film: {str(e)}")
