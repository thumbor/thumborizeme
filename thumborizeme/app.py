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
    application.listen(int(sys.argv[1]))
    tornado.ioloop.IOLoop.instance().start()
