import sys
import os.path

import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
settings = dict(
    static_path=root_path,
    template_path=root_path
)

application = tornado.web.Application([
    (r"/", MainHandler),
], **settings)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    else:
        port = int(sys.argv[1])

    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()
