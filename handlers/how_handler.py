import webapp2
from google.appengine.ext.webapp import template

class HowItWorksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(template.render('./html/how_it_works.html',''))
        