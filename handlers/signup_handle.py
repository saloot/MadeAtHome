import webapp2
from madeathome_forms import form_login
from utils import *
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from dbs.databases import UserPass_Chef
from dbs.databases import UserPass_User 

class SignUpHandler(webapp2.RequestHandler):               
        
    def get(self):
        
        signup_templ_params={}
        self.response.out.write(template.render('./html/login.html',signup_templ_params))            
                 


    def post(self):           
        signup_templ_params = {}
        user_flag = valid_name(self.request.get('username'))
        password_flag = valid_pass(self.request.get('password'))
        password_verify_flag = valid_pass(self.request.get('verify'))
        original_url = self.request.get('original_url')                
        signup_success_flag = 1
            
        if user_flag:
            user_name = self.request.get('username')            
            d = db.GqlQuery("SELECT * FROM UserPass_User WHERE user_id = '%s' " % user_name.lower())
            l = d.get()
                                        
            if (l):
                signup_success_flag = 0
                signup_templ_params['error_username_signup'] = "Sorry this username is already taken!"
            else:
                signup_templ_params['username_value_signup'] = str(user_name)
        else:
            signup_success_flag = 0
            signup_templ_params['error_username_signup'] = "Username is invalid"            

        if password_flag:         
            user_password = self.request.get('password')
        else:
            user_password = ""
            signup_success_flag = 0
            signup_templ_params['error_password_signup'] = "Invalid password!"
            
        if password_verify_flag:
            user_password_verify = self.request.get('verify')
        else:
            user_password_verify = ""
            signup_success_flag = 0
        
        if not (user_password == user_password_verify):
            signup_success_flag = 0
            signup_templ_params['error_password_verify_signup'] = "Passwords should match!"
            

        if (signup_success_flag):            
            hashed_val = make_hashed_cookie(user_name)
            self.response.headers.add_header('Set-Cookie','user_id=%s' % str(hashed_val))
            q = UserPass_User(user_id = user_name.lower(),user_pass = make_hashed_pw(user_name.lower(),
            user_password),ischef=0,user_bonus=0)
            q.put()
            time.sleep(2)
            self.redirect('/welcome')
        else:
                self.response.out.write(template.render('./html/login.html',signup_templ_params))
            
