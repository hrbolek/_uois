import tornado.ioloop
import tornado.web

class ApiHandler(tornado.web.RequestHandler):
#    def set_default_headers(self):
#        self.set_header("Content-Type", 'application/json')

    def prepare(self):
        self.args = None
        if 'Content-Type' in self.request.headers:
            if self.request.headers['Content-Type'] == 'application/x-json':
                self.args = json.loads(self.request.body)


    def get(self):
        if (not self.args is None):
            self.write(self.args)
        else:
            self.write('I am ok, thanks!')

def make_app():
    return tornado.web.Application([
        (r"/apit/", ApiHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()

print('Tornado probably up')