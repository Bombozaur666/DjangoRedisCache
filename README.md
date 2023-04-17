
# DjangoRedisCache

Simple app which will take url, send request to url and store response in cache for specific time.


## Environment Variables

To run this project, you will not need to add any environment variables. They all are stored in env dir. The are publicated only to help with local run. 

`SECRET_KEY_VALUE` Django secret key

`SERVER_IP` server ip at which it will be running

`PORT` server port at which it will be running

`CACHE_TTL` time in secunds. Describe how long data will be stored in cache
## Run Locally

Clone the project

```bash
  git clone https://github.com/Bombozaur666/DjangoRedisCache
```

Build Containers

```bash
  docker-compose build
```

To start server 

```bash
  docker-compose up
```

To start server in detached mode
```bash
  docker-compose up -d
```

To start server and get acces to all logs generated ONLY by a Django

```bash
  docker-compose run --service-ports server 
```


## Running Tests

To run tests, run the following command

```bash
  docker-compose run --service-ports server pytest -rP
```


## API Reference

#### Get all items

```http
  GET /ping/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `url` | `string` | **Required**. App will connect to this url |

It should be in request Body. Here is how to add it:

```json
{
    "url": "value"
}
```


