# Asynchronous Tasks with FastAPI and Celery

Example of how to handle background processes with FastAPI, Celery, and Docker.

## Want to learn how to build this?

Check out the [post](https://testdriven.io/blog/fastapi-and-celery/).

## Want to use this project?

Spin up the containers:

```sh
$ docker-compose up -d --build
```

Open your browser to [http://localhost:8004](http://localhost:8004) to view the app or to [http://localhost:5556](http://localhost:5556) to view the Flower dashboard.

Trigger a new task:

```sh
$ curl http://localhost:8004/tasks -H "Content-Type: application/json" --data '{"type": 0}'
```

Check the status:

```sh
$ curl http://localhost:8004/tasks/<TASK_ID>
```

#### Project Structure
The project structure and supporting source code are designed to implement semantic versioning.
```bash
.
project/
├── backend/
│   ├── .venv
│   ├── .env
│   ├── .gitignore
│   ├── requirements.txt
│   ├── app/
│   │   ├── app/
│   │   │   ├── api/
│   │   │   │   ├── v1/
│   │   │   │   │   └── summarize.py
|   |   |   |   |   └── summary_tasks.py
│   │   │   │   └── v2/
│   │   │   │       └── summaries.py
│   │   │   ├── database/
│   │   │   │   └── database.py
│   │   │   ├── models/
│   │   │   │   └── models.py
│   │   │   ├── schemas/
│   │   │   │   └── schemas.py
│   │   │   └── main.py
│   │   └── celery_app.py
│   │   └── celery.log
│   │   └── test.db
│   │   └── test
│   └── requirements.txt
└── frontend/
```
