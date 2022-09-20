import lxml.html
import json

from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.web import RequestHandler


class ReportHandler(RequestHandler):
    def __init__(self, application, request, **kwargs):
        self.redis_client = application.redis_client
        self.config = application.config

        super(ReportHandler, self).__init__(application, request, **kwargs)

    async def get(self):
        site_url = self.get_argument("url")

        cached_data = self.redis_client.get(site_url.rstrip("/"))
        if cached_data is not None:
            print("GETTING FROM CACHE")
            self.write(json.loads(cached_data))
            self.finish()
            return

        response = await self.get_content(site_url)
        html = lxml.html.fromstring(response.body)
        imgs = html.cssselect("img[src]")

        images = {}
        for img in imgs:
            url = img.get("src").lstrip("//")

            if not url.startswith("http"):
                url = f"{site_url.rstrip('/')}/{url}"
                if "data:image" in url:
                    continue

            print(f"Loading {url}...")

            try:
                if url in images:
                    continue

                loaded = await self.get_content(url)

                if loaded.code != 200:
                    continue
                original_size = len(loaded.body)

                webp = f"{self.config.get('THUMBOR_HOST')}/unsafe/filters:strip_icc():format(webp):quality(80)/{url}"
                webp_loaded = await self.get_content(webp)

                if webp_loaded.code != 200:
                    continue
                webp_size = len(webp_loaded.body)

                images[url] = {
                    "original": original_size / 1024.0,
                    "webp": webp_size / 1024.0,
                }

            except Exception as err:
                print(err)
                continue

        self.redis_client.incrby("total_images", len(images.keys()))

        json_data = json.dumps(
            {
                "url": site_url,
                "images-count": len(images.keys()),
                "images-size": round(
                    sum([image["original"] for image in images.values()]), 2
                ),
                "images-webp-size": round(
                    sum([image["webp"] for image in images.values()]), 2
                ),
            }
        )

        self.redis_client.setex(site_url.rstrip("/"), 6 * 60 * 60, json_data)

        self.write(json_data)

        self.finish()

    async def get_content(self, url):
        proxy_host = self.config.get("PROXY_HOST")
        if url.startswith("https"):
            proxy_host = self.config.get("PROXY_HOST_HTTPS")

        req = HTTPRequest(
            url=url,
            connect_timeout=3,
            request_timeout=10,
            proxy_host=proxy_host,
            proxy_port=int(self.config.get("PROXY_PORT")),
        )

        return await AsyncHTTPClient().fetch(req)
