#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# Simple, easy to use web server.
# 
# Just hand it a list of URL patterns (regexes) along with their
# handler functions do_get(path, response) and you're done.
# 
import re
import BaseHTTPServer
import os
import time
import random
import urlparse
import urllib
import cgi
import socket
from hashlib import sha1 as sha
from cPickle import load, dump

SESSION_PATH = "/tmp/sessions"

passwd_name = "/home/schemitz/Web/cgi-bin/passwd.dump"

class Request(object):
    def __init__(self, url, param, postvars, session):
        self.url = url
        self.param = param
        self.postvars = postvars
        self.session = session


def not_found(request, response):
    response["response"] = 404
    response["header"] = [ ("Content-type", "text/html; charset=utf-8"), ]
    response["data"] = ""


def static_file(path, content_type, cached=True):
    """ Serve a file from disk. If cached, the file is read once on
        startup; uncached, the file is read on every access.
    """
    if cached:
        file_content = file(path, "rb").read()
        def _cached_file_loader(request, response):
            response["response"] = 200
            response["header"] = [ ("Content-type", content_type), ]
            response["data"] = file_content
        return _cached_file_loader
    else:
        file_path = path
        def _uncached_file_loader(request, response):
            response["response"] = 200
            response["header"] = [ 
                ("Content-type", content_type),
                ("Cache-Control", "no-store"),
            ]
            response["data"] = file(file_path, "rb").read()
        return _uncached_file_loader


def run(url_map, host="127.0.0.1", port=8000):
    """ Run a web server, serving the URLs in the url_map with
        the associated handlers. The url_map contains pairs of
        regular expression patterns and handler functions, with
        a handler function taking two arguments, path and response.
        The response is a dict with the keys "response" (response
        code, default 404), "header" (a list of header name/value
        pairs), and "data" (the actual response data, default None).
    """

    sessions = { }
    users = { }

    # Inner class to pass URL map to.
    class GetHandler(BaseHTTPServer.BaseHTTPRequestHandler):

        def do_POST(self):
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                postvars = cgi.parse_multipart(self.rfile, pdict)
            elif ctype == 'application/x-www-form-urlencoded':
                length = int(self.headers.getheader('content-length'))
                postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
            else:
                postvars = {}
            self.do_GET(postvars)

        def do_GET(self, postvars=None):
            if self.path.find("?") >= 0:
                path = self.path[:self.path.find("?")]
                # in theory, this is the right way to obtain and decode 
                # request parameters; in practice, it fucks up UTF8 chars
                # even if they are properly URL-encoded...
                # http://unspecified.wordpress.com/2008/05/24/uri-encoding/
                #param = urlparse.parse_qs(self.path[self.path.find("?")+1:])
                param = {}
                for par in self.path.split("?")[1].split("&"):
                    parts = par.split("=")
                    k = parts[0]
                    if len(parts) == 2:
                        v = urllib.unquote(parts[1]).decode("utf8")
                    else:
                        v = u""
                    param.setdefault(k, []).append(v)
            else:
                path = self.path
                param = {}
            #print "URI: %s, args: %r" % (path, param)
            cookie = self.headers.getheader("Cookie") or "sid="
            #print "cookie line:", cookie
            cookie, sid = cookie.split("=")
            if cookie != "sid": sid = None
            #print "cookie token:", cookie
            if not sid:
                #print "generating new sid"
                hash = sha()
                hash.update("%i and %f" % (int(1000000000*random.random()), time.time()))
                sid = hash.hexdigest()
                sessions[sid] = dict(sid=sid, user=None)
            #print "sid:", sid
            s_name = os.path.join(SESSION_PATH, sid + ".dump")
            session = sessions.setdefault(sid, None)
            if not session:
                try:
                    session = load(file(s_name, "rb"))
                except IOError, ex:
                    # TODO: think real hard if this might pose an attack
                    # vector of chosen session ID attacks...?
                    #print "generating new session for old sid"
                    sessions[sid] = session = dict(sid=sid, user=None)
            if path == "/authenticate":
                user = param.get("user", [None])[0]
                password = param.get("password", [None])[0]
                redirect = param.get("redirect", [None])[0]
                print "user: %r, password: %r, redirect to: %r" \
                      % (user, password, redirect)
                pw_hash = sha()
                pw_hash.update(user + password)
                pw_hash = pw_hash.hexdigest()
                correct_hash = load(file(passwd_name, "rb")).get(user, None)
                if correct_hash is not None and pw_hash == correct_hash:
                    session["user"] = user
                    print "login as user %s successful" % user
                else:
                    session["user"] = None
                    redirect = "/login?error=login_failed"
                self.send_response(302)
                self.send_header("Set-Cookie", "sid=%s; path=/" % sid)
                self.send_header("Location", redirect)
                self.end_headers()
                dump(session, file(s_name, "wb"))
                return
            do_get = None
            for url_pattern, do_get_func in url_map:
                pattern = re.compile(url_pattern)
                if pattern.match(path):
                    do_get = do_get_func
                    break
            response = {
                "response": 404,
                "header": [],
                "data": None,
            }
            try:
                if do_get:
                    do_get(Request(path, param, postvars, session), response)
                if response["response"] == 404:
                    print "404: %r" % self.path
                    self.send_error(404, "File not found")
                self.send_response(response["response"])
                self.send_header("Set-Cookie", "sid=%s; path=/" % sid)
                self.send_header("Cache-Control", "no-store, no-cache, max-age=1")
                for header, value in response["header"]:
                    self.send_header(header, value)
                self.end_headers()
                if response["data"]:
                    self.wfile.write(response["data"])
            except KeyboardInterrupt, ex:
                raise ex
            except socket.error, ex:
                # well, that's all water under thw bridge now...
                pass
            except IOError, ex:
                if ex.errno == errno.EPIPE:
                    pass
                raise ex
            #except Exception, ex:
            #    print ex
            #    self.send_error(500, "Internal server error")
            dump(session, file(s_name, "wb"))

    import os
    try:
        os.mkdir(SESSION_PATH)
    except OSError:
        pass
    # Instantiate HTTP server class on port with the
    # inner handler class, thus implicitly passing the
    # url_map.
    httpd = BaseHTTPServer.HTTPServer((host, port), GetHandler)
    print "serving at: %s:%i" % (host, port)
    httpd.serve_forever()



### TEST CASE ###

import cgi, random


def test_do_get_quote(request, response):
    test_messages = [
        "That's as maybe, it's still a frog.",
        "Albatross! Albatross! Albatross!",
        "It's Wolfgang Amadeus Mozart",
        "A pink form from Reading.",
        "Hello people, and welcome to 'It's a Tree'",
        "I simply stare at the brick and it goes to sleep.",
    ]
    if request.url != "/": return
    tagline = random.choice(test_messages)
    data = """
<html>
<body>
  <p>
  Today's quote: <i>""" + cgi.escape(tagline) + """</i>
</body>
</html>
    """
    response["response"] = 200
    response["header"] = [ ("Content-type", "text/html"), ]
    response["data"] = data

def test_do_get_bla(request, response):
    data = """
<html>
<body>
  <p>
  bla-path: <i>""" + cgi.escape(request.url) + """</i>
  <p>
  sid: <i>""" + request.session["sid"] + """ </i>
</body>
</html>
    """
    response["response"] = 200
    response["header"] = [ ("Content-type", "text/html"), ]
    response["data"] = data

def favicon(request, response):
    img = file("/usr/share/icons/gnome-brave/16x16/stock/stock_person.png", "rb").read()
    response["response"] = 200
    response["header"] = [ ("Content-type", "image/png"), ]
    response["data"] = img

def test_login(request, response):
    data = """
<html>
<body>
  <form method="get" action="/authenticate">
  <input name="user" type="text" size="32" value="" />
  <input name="password" type="password" size="64" value="" />
  <input name="redirect" type="hidden" value="/bla2" />
  <input type="submit" value="Login" />
  </form>
  sid: <i>""" + request.session["sid"] + """ </i>
</body>
</html>
    """
    response["response"] = 200
    response["header"] = [ ("Content-type", "text/html"), ]
    response["data"] = data

if __name__ == "__main__":
    test_url_map = [
        ("/login", test_login),
        ("/favicon", favicon),
        ("/bla.*", test_do_get_bla),
        ("/", test_do_get_quote),
    ]
    run(test_url_map)

