import webapp2
from madeathome_forms import form_login
from utils import *
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from dbs.databases import UserPass_Chef
from dbs.databases import UserPass_User 

class SignUpHandler(webapp2.RequestHandler):               
        
    def get(self):
        cu_param = self.request.get('u')
        if cu_param:        
            if cu_param == 'user':
                params = ["","","","","","","","","","","",""]
                signup_templ_params= {"error_first_name": params[0],"error_last_name": params[1],"error_postal_address": params[2],
                "error_username": params[3], "error_password":params[4], "error_password_verify":params[5], "error_email":params[6],
                "first_name_value":params[7],"last_name_value":params[8],"postal_address_value":params[9],"username_value":params[10],
                "email_value":params[11]}
                self.response.out.write(template.render('./html/signup_user.html',signup_templ_params))
            elif cu_param == 'chef':
                params = ["","","","","","","","","","","","","","","",""]
                signup_templ_params= {"error_first_name": params[0],"error_last_name": params[1],"error_postal_address": params[2],
                "error_username": params[3], "error_password":params[4], "error_password_verify":params[5], "error_email":params[6],
                "first_name_value":params[7],"last_name_value":params[8],"postal_address_value":params[9],"username_value":params[10],
                "email_value":params[11],"paypal_email":params[12],"error_paypal_email":params[13],"cell_phone":params[14]
                 ,"error_cellphone":params[15]}
                self.response.out.write(template.render('./html/signup_chef.html',signup_templ_params))
            else:
                self.response.out.write('Invalid option!')
        else:
            self.response.out.write(template.render('./html/signup.html',''))
                 


    def post(self):           
        cu_param = self.request.get('u')
        if cu_param:
            if cu_param == 'chef':  
                params = ["","","","","","","","","","","","","","","",""]
                user_first_name = self.request.get('first_name')     
                user_last_name = self.request.get('last_name')
                user_postal_address = self.request.get('postal_address')                
                first_name_flag = valid_name(user_first_name)     
                last_name_flag = valid_name(user_last_name)     
                postal_address_flag = valid_address(user_postal_address)     
                user_flag = valid_name(self.request.get('username'))
                password_flag = valid_pass(self.request.get('password'))
                password_verify_flag = valid_pass(self.request.get('verify'))
                user_email = self.request.get('email')
                user_paypal_email = self.request.get('paypl')
                userphone = str(self.request.get('cellphone'))
                signup_success_flag = 1
        
                params[7] = str(user_first_name)
                params[8] = str(user_last_name)
                params[9] = str(user_postal_address)
                params[12] = str(user_paypal_email)
                params[14] = str(userphone)
        
                if user_email:
                    if (valid_email(user_email)):
                        params[11] = str(user_email)
                    else:
                        signup_success_flag = 0
                        params[6] = "Email is invalid"
                if user_paypal_email:
                    if (valid_email(user_paypal_email)):
                        params[12] = str(user_paypal_email)
                    else:
                        signup_success_flag = 0
                        params[13] = "Paypal address is invalid"
                    
                if userphone:
                    if (valid_phone(userphone)):
                        params[14] = userphone
                    else:
                        signup_success_flag = 0
                        params[15] = "Invalid phone number"
                            
                if not first_name_flag:                    
                    signup_success_flag = 0
                    params[0] = "Invalid first name!"

                if not last_name_flag:                    
                    signup_success_flag = 0
                    params[1] = "Invalid last name!"    
        
                if not postal_address_flag:                    
                    signup_success_flag = 0
                    params[2] = "Invalid postal address!"        
            
            
                if user_flag:
                    user_name = self.request.get('username')            
                    d = db.GqlQuery("SELECT * FROM UserPass_Chef WHERE user_id = '%s' " % user_name.lower())
                    l = d.get()     
                    if l:
                        signup_success_flag = 0
                        params[3] = "Sorry this username is already taken!"                
                    else:
                        params[10] = str(user_name)
                else:
                    signup_success_flag = 0
                    params[3] = "Username is invalid"            

                if password_flag:         
                    user_password = self.request.get('password')
                else:
                    user_password = ""
                    signup_success_flag = 0
                    params[4] = "Invalid password!"
            
                if password_verify_flag:
                    user_password_verify = self.request.get('verify')
                else:
                    user_password_verify = ""
                    signup_success_flag = 0
        
                if not (user_password == user_password_verify):
                    signup_success_flag = 0
                    params[5] = "Passwords shoudl match!"
            

                if (signup_success_flag):            
                    hashed_val = make_hashed_cookie(user_name)
                    self.response.headers.add_header('Set-Cookie','user_id=%s' % str(hashed_val))  
                    corrd = get_geolocation(user_postal_address) 
                    self.response.out.write(user_paypal_email)
                    q = UserPass_Chef(user_id = user_name.lower(),user_pass = make_hashed_pw(user_name.lower(),
                    user_password),user_firstname = user_first_name,user_lastname = user_last_name,
                    user_address = user_postal_address,user_email=user_email,user_latitude = corrd[0],user_longitude=corrd[1],user_phone=userphone,user_bankacnt=user_paypal_email)
                    q.put()                                            
                    self.redirect('/welcome')
                else:
                    signup_templ_params= {"error_first_name": params[0],"error_last_name": params[1],"error_postal_address": params[2],
                        "error_username": params[3], "error_password":params[4], "error_password_verify":params[5], "error_email":params[6],
                        "first_name_value":params[7],"last_name_value":params[8],"postal_address_value":params[9],"username_value":params[10],
                        "email_value":params[11],"paypal_email":params[12],"error_paypal_email":params[13],"cell_phone":params[14]
                        ,"error_cellphone":params[15]}
                    self.response.out.write(template.render('./html/signup_chef.html',signup_templ_params))
            elif cu_param == 'user':
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
                    
                    d2 = db.GqlQuery("SELECT * FROM UserPass_Chef WHERE user_id = '%s' " % user_name.lower())
                    l2 = d2.get()
                    
                    if (l or l2):
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
                    user_password))
                    q.put()                                            
                    self.redirect('/welcome')
                else:
                    
                    if (original_url == "/login"):                        
                        self.response.out.write(template.render('./html/login.html',signup_templ_params))                        
                    else:
                        self.response.out.write(template.render('./html/signup_user.html',signup_templ_params))

