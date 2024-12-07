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