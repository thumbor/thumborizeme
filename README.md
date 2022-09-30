# Thumborizeme

Thumborize is an application that shows the benefits of using the
[Thumbor](https://github.com/thumbor/thumbor).

## Configuration

To use redis some environments variables must be configured


##### Single Node
```python
REDIS_HOST = "localhost"
REDIS_DB = 0
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_MODE = "single_node"
```

##### Sentinel
```python
REDIS_SENTINEL_MASTER_INSTANCE = "redismaster"
REDIS_SENTINEL_MASTER_DB = 0
REDIS_SENTINEL_MASTER_PASSWORD = "dummy"
REDIS_SENTINEL_INSTANCES = "localhost:26379,localhost:26380"
REDIS_SENTINEL_PASSWORD = "dummy"
REDIS_SENTINEL_SOCKET_TIMEOUT = 1.0
REDIS_MODE = "sentinel"
```

## Dependencies

To install the dependencies, run the commands bellow:

```sh
make setup
```

## Run locally

To start thumborizeme, run the commands bellow:

```sh
make run
```
