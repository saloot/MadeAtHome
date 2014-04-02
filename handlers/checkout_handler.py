import webapp2
from google.appengine.ext.webapp import template
from dbs.databases import *
from utils import *

class CheckOutHandler(webapp2.RequestHandler):
    def get(self):
        params_checkout = {}
        
        #----------------------Check If a User Has Signed In-------------------------
        temp = self.request.cookies.get('user_id')
        if temp:
            userid = valid_hash_cookie(temp)
            if userid:
                params_checkout['userid'] = userid
                user = db.GqlQuery("SELECT * FROM UserPass_User WHERE user_id = '%s'" %userid)
                user = user.get()
                params_checkout['chef_flag'] = user.ischef
        #----------------------------------------------------------------------------
        
        
        params_checkout['home_site'] = "%s" %home_site  
        self.response.out.write(template.render('./html/check_out.html',''))
        