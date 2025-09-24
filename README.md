# Serverless-Lambda

A tiny FastAPI service to deploy, store, and execute short Python functions locally.  
Useful for demos and experiments — **not intended for running untrusted code in production**.

## Features
- Deploy functions (name + code) to a local SQLite database (`functions.db`)
- List, get, update, and delete functions
- Execute stored functions and return `stdout`/`stderr`
- Simple implementation using FastAPI + SQLAlchemy

## Quick Start (Windows `cmd.exe`)
1. Create and activate a virtual environment, then install dependencies:

        ```cmd
        python -m venv venv
        venv\Scripts\activate
        pip install -r requirements.txt
2.Start the server:
       
       ```cmd
        uvicorn main:app --reload
3.Open http://127.0.0.1:8000/docs  for the interactive API docs.

## API (high level)<br>
POST /deploy/ — deploy a function (body: { "name": "<name>", "code": "<python code>" })<br>
GET /functions/ — list all functions<br>
GET /function/{id} — get function by id<br>
PUT /function/{id} — update function (body: same as deploy)<br>
DELETE /function/{id} — delete function<br>
POST /execute/{id} — run the function and return output<br>

## Example (deploy + execute)<br>
Windows curl example (watch quoting):
       
       ```cmd
        curl -X POST "http://127.0.0.1:8000/deploy/" -H "Content-Type: application/json" -d "{\"name\":\"hello\",\"code\":\"print('Hello World')\"}"# response includes "function_id"
        curl -X POST "http://127.0.0.1:8000/execute/<function_id>"
Or use the Swagger UI at /docs.

## Tests<br>
Run tests from project root (venv activated):

        ```cmd
        python -m pytest -q
        
## Important notes<br>
Database: The SQLite DB functions.db is created in the project root. Do not commit this file; add it to .gitignore.<br>
Security: backend/executor.py executes submitted Python by writing to a temp file and running python temp.py. This is unsafe for untrusted input — only run trusted code locally.
