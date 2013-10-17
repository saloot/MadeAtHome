import webapp2
from madeathome_forms import form_login
from utils import *
from google.appengine.ext.webapp import template
from google.appengine.api import memcache
from google.appengine.ext import db


class LoginHandler(webapp2.RequestHandler):
    
    
    def get(self):
        temp = self.request.cookies.get('user_id')
        if temp:
            userid = valid_hash_cookie(temp)
            if userid:
                self.redirect('/welcome?u=chef')  
        else:
            params=["","","","unchecked"]
            login_templ_params= {"error_username": params[0], "error_password":params[1],"username_value":params[2],"check_box_val":params[3]}
            self.response.out.write(template.render('./html/login.html',login_templ_params))
            
            

    def post(self): 
        user_flag = valid_name(self.request.get('username'))
        password_flag = valid_pass(self.request.get('password'))
        remember_me_flag = self.request.get('remember_me_box')
        self.response.out.write(remember_me_flag)
        params = ["","","","unchecked"]
        success_flag = 1
        l = ""
#        print user_flag
        if not user_flag:
            params[0] = "Invalid username!"
            success_flag = 0
            user_name = self.request.get('username') 
            params[2] = user_name
        else:            
            user_name = self.request.get('username')  
            params[2] = str(user_name)
            d = db.GqlQuery("SELECT * FROM UserPass_User WHERE user_id = '%s' " % user_name.lower())
            l = d.get()
                 
            if not l:
                params[0] = "Username was not found"
                success_flag = 0                     
        if not password_flag:
            success_flag = 0
            params[1] = "Inavlid password"            
        else:
            user_password = self.request.get('password')
            if l:                
                h = l.user_pass            
                pass_check_flag = valid_hash_pw(user_name.lower(), user_password, h)
                if not pass_check_flag:                    
                    success_flag = 0
                    params[1] = "Username and password did not match!"    
            
            #print(success_flag)        
        if success_flag==1:            
            hashed_val = make_hashed_cookie(l.user_id)                
            if (remember_me_flag):
                cookee = Cookie.SimpleCookie()                  
                cookee['user_id'] = hashed_val
                cookee['user_id']['max-age'] = 14*24*3600
                expire_time_standard = 3600
                #print cookee
                cookie_str = 'user_id=%s;expires=' %str(hashed_val)
                cookie_str = cookie_str + str(expire_time_standard)
                self.response.headers.add_header('Set-Cookie',cookie_str)
            else:                    
                cookee = Cookie.SimpleCookie()                  
                cookee['user_id'] = hashed_val
                    #cookee['user_id']['max-age'] = 10
                #print cookee
                self.response.headers.add_header('Set-Cookie','user_id=%s' % str(hashed_val))
                
            self.redirect('/welcome')
        else:                
            login_templ_params= {"error_username": params[0], "error_password":params[1],"username_value":params[2],"check_box_val":params[3]}
            
            self.response.out.write(template.render('./html/login.html',login_templ_params))
