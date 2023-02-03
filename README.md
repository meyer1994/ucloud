# μCloud

Your own small cloud that can integrate with anything.

## About

I created this because I find complicated to have to deal with many complicated
interfaces from different service providers in order to have simple services
executing. Besides, I am always afraid of getting vendor locked...

## Integrations

Here is the current integrations table. I intend to add more as time goes.

|            | Rest | Files | Queue | Users (coming soon) |
|:-----------|:----:|:-----:|:-----:|:-------------------:|
| local      |      |   X   |       |                     |
| SQLite     |   X  |       |   X   |                     |
| PostgreSQL |   X  |       |   X   |                     |
| MongoDB    |   X  |       |   X   |                     |

## Installing

As easy as:

```
pip install -r requirements.txt
```

## Running

By default, we run with all backends locally, to make life easier for everyone
that just want to play around :)

```
uvicorn ucloud:app

INFO:     Started server process [111335]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

## Testing

We have two sets of tests: unit and integration. To run all tests, just execute
the following:

```
python -m unittest discover -vb tests
```

If you want to only execute unit/integration tests you can do the following:

```
python -m unittest discover -vb tests/unit  # or test/integration
```

## Configuration

As of now, all configurations can be changed using environment variables. More
info about all the configurations in the [settings][1] file. By default, all
configurations use `sqlite` and `local` where applicable.

### Rest

To select the REST backend, use the variable `UCLOUD_REST_TYPE`:

```
export UCLOUD_REST_TYPE=sqlite  # you can use 'postgresql' or 'mongodb'
export UCLOUD_REST_SQLITE_PATH=./my_rest_database
uvicorn ucloud:app
```

In the case for remote servers, like PostgreSQL or MongoDB, you simply use
similar named variable to point to the correct host:

```
export UCLOUD_REST_TYPE=postgresql
export UCLOUD_REST_POSTGRESQL_PATH=postgresql://postgres@127.0.0.1/postgres
```

### Queue

To select the queue backend, use the variable `UCLOUD_QUEUE_TYPE`:

```
export UCLOUD_QUEUE_TYPE=sqlite  # you can use 'postgresql' or 'mongodb'
export UCLOUD_QUEUE_SQLITE_PATH=./my_queue_database
uvicorn ucloud:app
```

### Files

To select the files backend, use the variable `UCLOUD_FILES_TYPE`:

```
export UCLOUD_FILES_TYPE=sqlite  # you can use 'postgresql' or 'mongodb'
export UCLOUD_FILES_LOCAL_PATH=./my_files_directory
uvicorn ucloud:app
```

[1]: ./ucloud/settings.py
