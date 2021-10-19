# Todos api

this api is a api with basic jwt auth with oauth2 

## About

<hr>

### `POST /token`

this is the route that takes a data payload and authenticate the user and sends a token as response

example

```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=string&password=string&scope=&client_id=&client_secret='
```

response

```sh
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJleHAiOjE2MzQ2NTM5MjN9.L3V02uClzR-ZtL5Kd6wEPWYx0TcHIMLVCqd58lNMJow",
  "token_type": "bearer"
}
```

<hr>

### `POST /user/create`

this route creates a new user for consuming the api, it take a data payload of  json returns a sucess message

example

```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/users/create' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "string",
  "email": "string",
  "disabled": true,
  "password": "string",
  "id": "string"
}'
```

response

```sh
"created succesfully"
```

<hr>

### `POST /todo/add`

this route take a json payload of `todo` and a `isCompleted` key value pair `isCompleted` been the status of the todo item  `todo` been the text message, and a `AUTHORIZATION HEADER`

example

```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/todo/add' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJleHAiOjE2MzQ2NTM0NTZ9.BpN8RRuzD0TmPOVSOLkJMf2EY2Bb3L7qqzOmAjSYt_0' \
  -H 'Content-Type: application/json' \
  -d '{
  "todo": "string",
  "isComplete": true
}'
```

response

```sh
"todo added"
```

<hr>

### `GET /todo/all`

this returns all the todos a user has 
it takes a `Header` of Authorization
and returns all the todos 

```sh
curl -X 'GET' \
  'http://127.0.0.1:8000/todo/all' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJleHAiOjE2MzQ2NTM0NTZ9.BpN8RRuzD0TmPOVSOLkJMf2EY2Bb3L7qqzOmAjSYt_0'
```

```sh
[
  {
    "text": "submit the project",
    "isCompleted": true,
    "id": "616ec5affd3ad8b1f1ee484d"
  },
  {
    "text": "watch tv or something",
    "isCompleted": true,
    "id": "616ec8da8a7342437fe49aa9"
  },
  {
    "text": "string",
    "isCompleted": true,
    "id": "616ed3e2b0aeeca56ce9770c"
  }
]
```

<hr>

### `PUT /todo/text/{todo_id}`

this is a dynamic uri it takes a  `AUTHORIZATION HEADER`
and the query as `text`

example

```sh
curl -X 'PUT' \
  'http://127.0.0.1:8000/todo/text/616eae617941dff929176b8e?todo_text=make%20a%20pull%20request' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJleHAiOjE2MzQ2NTU0MzV9.YEsxXcCP13bDkAp3PaDms53BqtSXuzZqrEofnr-Bwa0'
```

response 

```sh
"todo updated"
```

<hr>

### `PUT /todo/toggleComplete/{todo_id}`

this route is to toggle `isComplete` of a todo i.e the status of the todo it takes   `AUTHORIZATION HEADER`, the todo_id is the path

example

```sh
curl -X 'PUT' \
  'http://127.0.0.1:8000/todo/toggleComplete/616eae617941dff929176b8e' \
  -H 'accept: application/json'
```

response

```sh
"todo updated"
```

<hr>

### `DELETE /todo/{todo_id}`

this api is response for deleteing todos
the path is todo_id 

example

```sh
curl -X 'DELETE' \
  'http://127.0.0.1:8000/todo/616eae617941dff929176b8e' \
  -H 'accept: application/json'
```

response

```sh
"todo delete"
```

<hr>

## Data Model

### User document 

mongodb adds id implicitly so we are not adding it here

| Field      | Type |
| ----------- | ----------- |
| username      | string       |
| email   | string        |
| password | string |
| disabled | boolean|

### Todos document

| Field      | Type |
| ----------- | ----------- |
| text      | string       |
| isCompleted   | boolean        |
| userid | string |

## Installation

### First clone the repo

```sh
git clone <repo-name>.git
```

### Get dependencies

```sh
pip install -r requirements.txt
```

### Run the project

```sh
uvicorn main:app --reload 
```

### Know more route to 

https://127.0.0.1:8000/docs