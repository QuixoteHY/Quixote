# https://blog.csdn.net/midion9/article/details/51332973

# curl -L -e '; auto' http://localhost:8000/

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path
import time

from tornado.web import HTTPError, _time_independent_equals, utf8

from tornado.options import define, options

# 119.29.152.194

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

    def set_secure_cookie(self, name, value, expires_days=30, version=None, **kwargs):
        """Signs and timestamps a cookie so it cannot be forged.

        You must specify the ``cookie_secret`` setting in your Application
        to use this method. It should be a long, random sequence of bytes
        to be used as the HMAC secret for the signature.

        To read a cookie set with this method, use `get_secure_cookie()`.

        Note that the ``expires_days`` parameter sets the lifetime of the
        cookie in the browser, but is independent of the ``max_age_days``
        parameter to `get_secure_cookie`.

        Secure cookies may contain arbitrary byte values, not just unicode
        strings (unlike regular cookies)

        Similar to `set_cookie`, the effect of this method will not be
        seen until the following request.

        .. versionchanged:: 3.2.1

           Added the ``version`` argument.  Introduced cookie version 2
           and made it the default.
        """
        self.set_cookie(name, self.create_signed_value(name, value,
                                                       version=version),
                        expires_days=None, **kwargs)

    def check_xsrf_cookie(self):
        token = (self.get_argument("_xsrf", None) or
                 self.request.headers.get("X-Xsrftoken") or
                 self.request.headers.get("X-Csrftoken"))
        print('token: '+str(token))
        if not token:
            raise HTTPError(403, "'_xsrf' argument missing from POST")
        _v, token, _t = self._decode_xsrf_token(token)
        print(_v, 'token: '+str(token), _t)
        _v, expected_token, _t = self._get_raw_xsrf_token()
        print(_v, 'expected_token: '+str(expected_token), _t)
        if not token:
            raise HTTPError(403, "'_xsrf' argument has invalid format")
        if not _time_independent_equals(utf8(token), utf8(expected_token)):
            raise HTTPError(403, "XSRF cookie does not match POST argument")

    def _get_raw_xsrf_token(self):
        print('*'*30+' _get_raw_xsrf_token')
        print('RequestHandler ID: '+str(id(self)))
        print(self.request.cookies)
        if not hasattr(self, '_raw_xsrf_token'):
            cookie = self.get_cookie("_xsrf")
            print(cookie)
            if cookie:
                version, token, timestamp = self._decode_xsrf_token(cookie)
                print('Y: ', version, token, timestamp)
            else:
                version, token, timestamp = None, None, None
                print('N: ', version, token, timestamp)
            if token is None:
                version = None
                token = os.urandom(16)
                timestamp = time.time()
                print('New: ', version, token, timestamp)
            self._raw_xsrf_token = (version, token, timestamp)
        print('*'*30+' _get_raw_xsrf_token')
        return self._raw_xsrf_token


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
