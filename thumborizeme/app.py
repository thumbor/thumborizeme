import tornado.web
import os

from thumborizeme.settings import Settings
from thumborizeme.handlers.report import ReportHandler
from thumborizeme.handlers.healthcheck import HealthCheckHandler
from thumborizeme.handlers.home import HomeHandler
from thumborizeme.redis_client import RedisClient


class ThumborizemeApp(tornado.web.Application):
    def __init__(self):
        self.config = Settings()
        self.redis_client = RedisClient(self.config).initialize()

        root = os.path.dirname(__file__)
        handlers = [
            (
                r"/",
                HomeHandler,
            ),
            (r"/report", ReportHandler),
            (r"/healthcheck", HealthCheckHandler),
            (
                "/static/(.*)",
                tornado.web.StaticFileHandler,
                {"path": root + "/static"},
            ),
        ]

        super(ThumborizemeApp, self).__init__(handlers, static_path=root + "/static")
