from datetime import datetime

from tornado.web import RequestHandler


class HomeHandler(RequestHandler):
    def __init__(self, application, request, **kwargs):
        self.redis_client = application.redis_client
        self.config = application.config

        super(HomeHandler, self).__init__(application, request, **kwargs)

    async def get(self):
        url = self.get_argument("url", None)

        if url is None:
            title = "Check how you would benefit from using thumbor"
        else:
            title = f"Test results for {url}"

        total_images = self.redis_client.get("total_images")
        total_images = int(total_images or 0)

        year = datetime.now().year

        self.render(
            "../static/index.html",
            title=title,
            total_images=total_images,
            year=year,
            host=self.config.get("HOST"),
            thumbor_host=self.config.get("THUMBOR_HOST"),
        )
