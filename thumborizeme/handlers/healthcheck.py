from tornado.web import RequestHandler


class HealthCheckHandler(RequestHandler):
    def __init__(self, application, request, **kwargs):
        self.redis_client = application.redis_client

        super(HealthCheckHandler, self).__init__(application, request, **kwargs)

    async def get(self):
        try:
            self.redis_client.ping()
            self.write("WORKING !")
        except Exception:
            self.set_status(500)
            self.write("DOWN !")
        self.finish()
