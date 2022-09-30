import tornado.ioloop

from thumborizeme.app import ThumborizemeApp


def main():
    app = ThumborizemeApp()
    port = app.config.get("PORT", 8999)
    app.listen(port)
    print(f"Thumborizeme App listening on port: {port}")
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
