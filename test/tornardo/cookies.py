# https://blog.csdn.net/midion9/article/details/51332973

# curl -L -e '; auto' http://localhost:8000/

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)

check_dict = {
    'huyuan': 'hy195730',
    'quixote': '123456789',
}


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        temp = self.get_secure_cookie("username")
        print('get_current_user: '+str(temp))
        return temp


class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        if username in check_dict and password == check_dict[username]:
            self.set_secure_cookie("username", username)
            self.redirect("/welcome")
        else:
            self.redirect("/login")


class WelcomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('index.html', user=self.current_user)


class TestCookiesHandler(BaseHandler):
    # http://localhost:8000/test_cookies/34232534
    @tornado.web.authenticated
    def get(self, input_number):
        # self.write("Welcome to quixote, your number is %s." % str(input_number))
        self.render('test_cookies.html', user=self.current_user, input_number=str(input_number))


class LogoutHandler(BaseHandler):
    def get(self):
        if self.get_argument("logout", None):
            self.clear_cookie("username")
            self.redirect("/")


if __name__ == "__main__":
    tornado.options.parse_command_line()

    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "xsrf_cookies": True,
        "login_url": "/login"
    }

    application = tornado.web.Application([
        (r'/', WelcomeHandler),
        (r'/welcome', WelcomeHandler),
        (r'/login', LoginHandler),
        (r'/logout', LogoutHandler),
        (r"/test_cookies/(\w+)", TestCookiesHandler),
    ], **settings)

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
