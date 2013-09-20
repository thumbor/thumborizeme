import sys
import os.path
from json import dumps, loads
from datetime import datetime

import tornado.ioloop
import tornado.web
import tornado.gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.concurrent import return_future
import lxml.html
from toredis import Client


class MainHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    @tornado.web.asynchronous
    def get(self):
        url = self.get_argument('url', None)

        if url is None:
            title = "Check how you would benefit from using thumbor"
        else:
            title = "Test results for %s" % url

        total_images = yield tornado.gen.Task(self.application.redis.get, 'total_images')
        total_images = int(total_images or 0)

        self.render('index.html', title=title, total_images=total_images)
        self.finish()


class GetReportHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    @tornado.web.asynchronous
    def get(self):
        site_url = self.get_argument('url')

        cached_data = yield tornado.gen.Task(self.application.redis.get, site_url.rstrip('/'))
        if cached_data is not None:
            print "GETTING FROM CACHE"
            self.write(loads(cached_data))
            self.finish()
            return

        response = yield self.get_content(site_url)

        html = lxml.html.fromstring(response.body)
        imgs = html.cssselect('img[src]')

        images = {}

        for img in imgs:
            url = img.get('src').lstrip('//')

            if not url.startswith('http'):
                url = "%s/%s" % (site_url.rstrip('/'), url)

            print "Loading %s..." % url

            try:
                if url in images:
                    continue

                loaded = yield self.get_content(url)
                if loaded.code != 200:
                    continue
                original_size = len(loaded.body)

                #thumborized = "http://thumbor.thumborize.me/unsafe/filters:strip_icc()/%s" % url
                #print "Loading thumborized %s..." % thumborized
                #loaded = yield http_client.fetch(thumborized)
                #thumborized_size = len(loaded.body)

                webp = "http://thumbor.thumborize.me/unsafe/filters:strip_icc():format(webp):quality(80)/%s" % url
                #print "Loading webp %s..." % webp
                loaded = yield self.get_content(webp)
                if loaded.code != 200:
                    continue
                webp_size = len(loaded.body)

                images[url] = {
                    'original': original_size / 1024.0,
                    #'thumborized': thumborized_size / 1024.0,
                    'webp': webp_size / 1024.0
                }

            except Exception, err:
                print str(err)
                continue

        yield tornado.gen.Task(self.application.redis.incrby, 'total_images', len(images.keys()))

        json_data = self.to_json({
            'url': site_url,
            'images-count': len(images.keys()),
            'images-size': round(sum([image['original'] for image in images.values()]), 2),
            'images-webp-size': round(sum([image['webp'] for image in images.values()]), 2)
        })

        yield tornado.gen.Task(self.application.redis.setex, site_url.rstrip('/'), 6 * 60 * 60, json_data)

        self.write(json_data)

        self.finish()

    def to_json(self, value):
        return dumps(value)

    @return_future
    def get_content(self, url, callback):
        req = HTTPRequest(
            url=url,
            connect_timeout=1,
            request_timeout=3,
        )

        http_client = AsyncHTTPClient()
        http_client.fetch(req, callback)

    def is_expired(self, dt):
        return (datetime.now() - dt).total_seconds() > (6 * 60 * 60)


def has_connected(application, io_loop):
    def handle(*args, **kw):
        pass

    return handle


def main(port):
    io_loop = tornado.ioloop.IOLoop.instance()

    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    settings = dict(
        static_path=root_path,
        template_path=root_path
    )

    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/report", GetReportHandler),
    ], **settings)

    redis_host = '127.0.0.1'
    redis_port = 6379

    application.redis = Client(io_loop=io_loop)
    application.redis.authenticated = False
    application.redis.connect(redis_host, redis_port, callback=has_connected(application, io_loop))

    application.listen(port)
    io_loop.start()


if __name__ == "__main__":
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    else:
        port = int(sys.argv[1])

    main(port)
