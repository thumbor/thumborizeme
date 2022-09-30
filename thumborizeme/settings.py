from pydantic import BaseSettings


class Settings(BaseSettings):
    PORT: int = 9000

    REDIS_MODE: str = "SINGLE_NODE"

    # REDIS
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = None
    REDIS_SERVER_DB: int = 0

    # REDIS SENTINEL
    REDIS_SENTINEL_MASTER_INSTANCE: str = "redismaster"
    REDIS_SENTINEL_MASTER_DB: int = 0
    REDIS_SENTINEL_MASTER_PASSWORD: str = None
    REDIS_SENTINEL_INSTANCES: str = "localhost:26379"
    REDIS_SENTINEL_PASSWORD: str = None
    REDIS_SENTINEL_SOCKET_TIMEOUT: float = 10.0

    HOST: str = "http://localhost:" + str(PORT)
    THUMBOR_HOST: str = "http://localhost:8888"

    # PROXY
    PROXY_HOST: str = ""
    PROXY_HOST_HTTPS: str = ""
    PROXY_PORT: int = 0

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        raise AttributeError(name)

    def get(self, name, default=None):
        if hasattr(self, name):
            return self.__getattr__(name)
        return default

    def __setattr__(self, name, value):
        self.__dict__[name] = value
