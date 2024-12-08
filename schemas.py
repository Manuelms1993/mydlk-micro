from pydantic import BaseModel
from typing import Optional

from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType


class FilmEntry(BaseModel):
    id: str = None
    title: Optional[str] = None
    type: Optional[str] = None
    release_year: Optional[int] = None
    age_certification: Optional[str] = None
    runtime: Optional[int] = None
    genres: Optional[str] = None
    production_countries: Optional[str] = None
    seasons: Optional[int] = None
    imdb_score: Optional[float] = None
    imdb_votes: Optional[int] = None
    tmdb_popularity: Optional[str] = None
    tmdb_score: Optional[float] = None

schemaFilmEntry = StructType([
    StructField("id", StringType(), False),
    StructField("title", StringType(), True),
    StructField("type", StringType(), True),
    StructField("release_year", IntegerType(), True),
    StructField("age_certification", StringType(), True),
    StructField("runtime", IntegerType(), True),
    StructField("genres", StringType(), True),
    StructField("production_countries", StringType(), True),
    StructField("seasons", IntegerType(), True),  # Nullable field
    StructField("imdb_score", FloatType(), True),
    StructField("imdb_votes", IntegerType(), True),
    StructField("tmdb_popularity", StringType(), True),
    StructField("tmdb_score", FloatType(), True)
])