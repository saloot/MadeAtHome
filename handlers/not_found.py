import webapp2
from google.appengine.ext.webapp import template

class NotFoundHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(template.render('./html/404.html',''))
        