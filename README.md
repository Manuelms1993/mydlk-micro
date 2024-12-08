# mydlk-micro


# REST API Methods Explained

This document provides an overview of common REST API methods, their purposes, and how they should be used in a RESTful web service.

---

## HTTP Methods Overview

| HTTP Method | Purpose                                           | Action on Data                   | Idempotent | Safe |
|-------------|---------------------------------------------------|-----------------------------------|------------|------|
| **GET**     | Retrieve data from the server                    | Read                             | Yes        | Yes  |
| **POST**    | Create a new resource or trigger an action       | Create/Submit Data               | No         | No   |
| **PUT**     | Update or create a resource                      | Replace entire resource          | Yes        | No   |
| **PATCH**   | Partially update a resource                      | Update part of a resource        | No         | No   |
| **DELETE**  | Delete a resource                                | Remove a resource                | Yes        | No   |
| **HEAD**    | Retrieve only the headers of a resource          | No body, just headers            | Yes        | Yes  |
| **OPTIONS** | Retrieve allowed communication methods for a resource | Return supported methods     | Yes        | Yes  |

---

## GET /get-imdb-film/

### Description

This endpoint retrieves a single row from a Hive table based on the specified schema, table name, and row ID. The result is returned as a JSON object, where the keys are column names and the values are the corresponding row data.

---

### Request Parameters

| Parameter Name | Type    | Required | Description                             |
|----------------|---------|----------|-----------------------------------------|
| `id`           | integer | Yes      | The unique identifier of the desired row.|

- **Request Type**: `GET`
- **Endpoint URL**: `/get-imdb-film/`

---

### Example Request

Using `cURL`:
```bash
curl "http://127.0.0.1:8054/get-imdb-film/?id=tm180542"
```

## GET /get-imdb-film-by-name/

### Description

This endpoint retrieves a single row from a Hive table based on the specified schema, table name, and row ID. The result is returned as a JSON object, where the keys are column names and the values are the corresponding row data.

---

### Request Parameters

| Parameter Name | Type   | Required | Description |
|----------------|--------|----------|-------------|
| `name`         | string | Yes      | name        |

- **Request Type**: `GET`
- **Endpoint URL**: `/get-imdb-film-by-name/`

---

### Example Request

Using `cURL`:
```bash
curl "http://127.0.0.1:8054/get-imdb-film-by-name/?name=Once%20Upon%20a%20Time%20in%20America"
```

## POST /create-film/

### Descripción

Este endpoint crea una nueva entrada en una tabla de Hive utilizando un payload JSON proporcionado. El endpoint está diseñado para insertar datos en la tabla de Hive `bi.films_imdb`, que almacena detalles sobre películas como su título, año de lanzamiento, géneros y calificaciones.

---

### Cuerpo de la Solicitud (Request Body)

El cuerpo de la solicitud debe ser un objeto JSON con el siguiente esquema:

| Nombre del Campo      | Tipo     | Requerido | Descripción                                     |
|-----------------------|----------|-----------|------------------------------------------------|
| `id`                 | string   | Sí        | Identificador único de la película.            |
| `title`              | string   | Sí        | Título de la película.                         |
| `type`               | string   | Sí        | Tipo de contenido (por ejemplo, "MOVIE").      |
| `release_year`       | integer  | Sí        | Año de lanzamiento de la película.             |
| `age_certification`  | string   | No        | Certificación de edad (por ejemplo, "R").      |
| `runtime`            | integer  | Sí        | Duración de la película en minutos.            |
| `genres`             | string   | Sí        | Lista de géneros en formato JSON string.       |
| `production_countries` | string | Sí        | Lista de países de producción en formato JSON string. |
| `seasons`            | integer  | No        | Número de temporadas (si aplica, de lo contrario `null`). |
| `imdb_score`         | float    | Sí        | Calificación de IMDb de la película.           |
| `imdb_votes`         | integer  | Sí        | Número de votos en IMDb.                       |
| `tmdb_popularity`    | string   | Sí        | Puntuación de popularidad de TMDB.             |
| `tmdb_score`         | float    | Sí        | Calificación de TMDB de la película.           |

---

### Tipo de Solicitud

- **Método**: `POST`  
- **URL del Endpoint**: `/create-film/`

---

### Ejemplo de Solicitud

Usando `cURL`:

```bash
curl -X POST "http://127.0.0.1:8054/create-film/" \
-H "Content-Type: application/json" \
-d '{
    "id": "tm999999",
    "title": "Deadpool vs lobezno",
    "type": "MOVIE",
    "release_year": 2024,
    "age_certification": "R",
    "runtime": 139,
    "genres": "[\"crime\", \"drama\", \"european\"]",
    "production_countries": "[\"US\", \"IT\"]",
    "seasons": 1,
    "imdb_score": 7.3,
    "imdb_votes": 345714,
    "tmdb_popularity": "25.937",
    "tmdb_score": 7.453
}'

curl "http://127.0.0.1:8054/get-imdb-film/?id=tm999999"
```

## PUT /insert-if-not-exist-film/

### Description

This endpoint inserts a new entry into the `bi.films_imdb` Hive table, provided the record does not already exist. It checks for an existing entry with the same `id`. If a record with the given `id` exists, it returns an error response. Otherwise, it appends the new record to the table.

---

### Request Body

The request body should be a JSON object with the following schema:

| Field Name            | Type    | Required | Description                                   |
|-----------------------|---------|----------|-----------------------------------------------|
| `id`                 | string  | Yes      | Unique identifier for the film.              |
| `title`              | string  | Yes      | Title of the film.                           |
| `type`               | string  | Yes      | Type of the content (e.g., "MOVIE").         |
| `release_year`       | integer | Yes      | Release year of the film.                    |
| `age_certification`  | string  | No       | Age certification (e.g., "R", "PG-13").      |
| `runtime`            | integer | Yes      | Runtime of the film in minutes.              |
| `genres`             | string  | Yes      | List of genres in JSON string format.        |
| `production_countries` | string | Yes    | List of production countries in JSON string format. |
| `seasons`            | integer | No       | Number of seasons (if applicable).           |
| `imdb_score`         | float   | Yes      | IMDb rating of the film.                     |
| `imdb_votes`         | integer | Yes      | Number of votes on IMDb.                     |
| `tmdb_popularity`    | string  | Yes      | Popularity score from TMDB.                  |
| `tmdb_score`         | float   | Yes      | TMDB rating of the film.                     |

---

### Request Type

- **Method**: `PUT`
- **Endpoint URL**: `/insert-if-not-exist-film/`

---

### Example Request

Using `cURL`:

```bash
curl -X PUT "http://127.0.0.1:8054/insert-if-not-exist-film/" \
-H "Content-Type: application/json" \
-d '{
    "id": "tm999999",
    "title": "Deadpool vs lobezno",
    "type": "MOVIE",
    "release_year": 2024,
    "age_certification": "R",
    "runtime": 139,
    "genres": "[\"crime\", \"drama\", \"european\"]",
    "production_countries": "[\"US\", \"IT\"]",
    "seasons": 1,
    "imdb_score": 7.3,
    "imdb_votes": 345714,
    "tmdb_popularity": "25.937",
    "tmdb_score": 7.453
}'
```

## PATCH /update-film/{film_id}

### Description

This endpoint allows for partially updating an existing film's entry in the `bi.films_imdb` Hive table. Only the fields provided in the request body will be updated, leaving other attributes unchanged. If the film with the specified `id` does not exist, a `404 Not Found` response will be returned.

---

### Request Parameters

| Parameter Name | Type   | Required | Description                               |
|----------------|--------|----------|-------------------------------------------|
| `film_id`      | string | Yes      | Unique identifier of the film to update.  |

### Request Body

The request body should be a JSON object with the fields you want to update. Only the fields that need to be updated should be provided.

| Field Name            | Type    | Required | Description                                   |
|-----------------------|---------|----------|-----------------------------------------------|
| `title`               | string  | No       | Updated title of the film.                   |
| `imdb_score`          | float   | No       | Updated IMDb score of the film.              |
| `release_year`        | integer | No       | Updated release year of the film.            |
| `genres`              | string  | No       | Updated genres list in JSON string format.   |
| `runtime`             | integer | No       | Updated runtime of the film in minutes.      |
| `tmdb_score`          | float   | No       | Updated TMDB score of the film.              |

---

### Request Type

- **Method**: `PATCH`
- **Endpoint URL**: `/update-film/{film_id}`

---

### Example Request

Using `cURL`:
```bash
curl -X PATCH "http://127.0.0.1:8054/update-film/tm180542" \
-H "Content-Type: application/json" \
-d '{
    "title": "Once Upon a Time in America (Updated)",
    "imdb_score": 8.5
}'

curl "http://127.0.0.1:8054/get-imdb-film/?id=tm180542"
```

## DELETE /delete-film/{film_id}

### Description
This endpoint deletes a specific film entry from the `bi.films_imdb` Hive table by removing the row with the given `film_id`. The deletion is performed using the `INSERT OVERWRITE` method, which overwrites the table with all rows except the one to be deleted.

### Request Parameters

| Parameter Name | Type   | Required | Description           |
|----------------|--------|----------|-----------------------|
| `film_id`      | string | Yes      | Unique identifier for the film. |

- **Request Type**: `DELETE`
- **Endpoint URL**: `/delete-film/{film_id}`

### Request Example

Using `cURL`:
```bash
curl -I "http://127.0.0.1:8054/delete-film/tm180542" # head

curl -X DELETE "http://127.0.0.1:8054/delete-film/tm999999"
```

