import webapp2
from google.appengine.ext.webapp import template
from utils import *

class CheckOutHandler(webapp2.RequestHandler):
    def get(self):
        params_checkout = {}
        params_checkout['home_site'] = "%s" %home_site  
        self.response.out.write(template.render('./html/check_out.html',''))
        