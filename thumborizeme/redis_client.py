from redis import Redis, RedisError, Sentinel

SINGLE_NODE = "single_node"
SENTINEL = "sentinel"


class RedisClient:
    def __init__(self, config):
        self.config = config

    def initialize(self):
        redis_mode = self.config.get("REDIS_MODE").lower()

        if redis_mode == SINGLE_NODE:
            return self.__redis_single_node_client()
        if redis_mode == SENTINEL:
            return self.__redis_sentinel_client()

        raise RedisError(f"REDIS_MODE must be {SINGLE_NODE} or {SENTINEL}")

    def __redis_single_node_client(self):
        return Redis(
            host=self.config.get("REDIS_HOST"),
            port=self.config.get("REDIS_PORT"),
            db=self.config.get("REDIS_DB"),
            password=self.config.get("REDIS_PASSWORD"),
        )

    def __redis_sentinel_client(self):
        instances_split = self.config.get("REDIS_SENTINEL_INSTANCES").split(",")
        instances = [tuple(instance.split(":")) for instance in instances_split]

        if self.config.get("REDIS_SENTINEL_PASSWORD"):
            sentinel_instance = Sentinel(
                instances,
                socket_timeout=self.config.get("REDIS_SENTINEL_SOCKET_TIMEOUT"),
                sentinel_kwargs={
                    "password": self.config.get("REDIS_SENTINEL_PASSWORD")
                },
            )
        else:
            sentinel_instance = Sentinel(
                instances,
                socket_timeout=self.config.get("REDIS_SENTINEL_SOCKET_TIMEOUT"),
            )
        # breakpoint()
        return sentinel_instance.master_for(
            self.config.get("REDIS_SENTINEL_MASTER_INSTANCE"),
            socket_timeout=self.config.get("REDIS_SENTINEL_SOCKET_TIMEOUT"),
            password=self.config.get("REDIS_SENTINEL_MASTER_PASSWORD"),
            db=self.config.get("REDIS_SENTINEL_MASTER_DB"),
        )
