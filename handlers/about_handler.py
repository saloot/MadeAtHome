import webapp2
from google.appengine.ext.webapp import template

class AboutUsHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(template.render('./html/about_us.html',''))
        