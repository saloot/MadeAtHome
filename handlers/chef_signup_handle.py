import webapp2
from madeathome_forms import form_login
from utils import *
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from dbs.databases import UserPass_Chef
from dbs.databases import UserPass_User 

class ChefSignUpHandler(webapp2.RequestHandler):               
        
    def get(self):
        
        signup_templ_params = {}
        temp = self.request.cookies.get('user_id')
        if temp:
            userid = valid_hash_cookie(temp)
            if userid:
                signup_templ_params['userid'] = userid
                d = db.GqlQuery("SELECT * FROM UserPass_User WHERE user_id = '%s' " %userid)
                l = d.get()
                #if l.user_first_name:
                #    signup_templ_params['first_name_value']= (l.user_firstname)
                #if l.user_last_name:
                #    signup_templ_params['last_name_value']= (l.user_last_name)
                #if l.user_address:
                #    signup_templ_params['postal_address_value'] = (l.user_address)
                #if l.user_email:
                #    signup_templ_params['email_value'] = (l.user_email)
                
            else:
                self.response.out.write('what the hell? invlaid user?!')
        else:
            self.response.out.write('what the hell? no user?!')
        self.response.out.write(template.render('./html/signup_chef.html',signup_templ_params))            
                 

    def post(self):
        signup_templ_params = {}
        temp = self.request.cookies.get('user_id')
        if temp:
            userid = valid_hash_cookie(temp)
            if userid:
                signup_templ_params['userid'] = userid
            else:
                self.response.out.write('what the hell? invlaid user?!')
        else:
            self.response.out.write('what the hell? no user?!')
          
        
        
        user_first_name = self.request.get('first_name')     
        user_last_name = self.request.get('last_name')
        user_postal_address = self.request.get('postal_address')
        restaraunt_val = self.request.get('restaraunt')
        
        first_name_flag = valid_name(user_first_name)
        last_name_flag = valid_name(user_last_name)
        restaurant_flag = valid_name(restaraunt_val)
        postal_address_flag = valid_address(user_postal_address)        
        
        user_email = self.request.get('email')
        user_paypal_email = self.request.get('paypl')
        userphone = str(self.request.get('cellphone'))
        
        signup_success_flag = 1
        
        signup_templ_params['first_name_value']= str(user_first_name)
        signup_templ_params['last_name_value']= str(user_last_name)
        signup_templ_params['postal_address_value'] = str(user_postal_address)
        signup_templ_params['paypal_email'] = str(user_paypal_email)
        signup_templ_params['cell_phone'] = str(userphone)
        signup_templ_params['restaraunt_value'] = restaraunt_val
        
        if user_email:
            if (valid_email(user_email)):
                signup_templ_params['email_value'] = str(user_email)
            else:
                signup_success_flag = 0
                signup_templ_params['error_email'] = "Email is invalid"
        if user_paypal_email:
            if (valid_email(user_paypal_email)):
                signup_templ_params['paypal_email'] = str(user_paypal_email)
            else:
                signup_success_flag = 0
                signup_templ_params['error_paypal'] = "Paypal address is invalid"
                    
        if userphone:
            if (valid_phone(userphone)):
                signup_templ_params['cell_phone'] = userphone
            else:
                signup_success_flag = 0
                signup_templ_params['error_cellphone'] = "Invalid phone number"
                            
        if not first_name_flag:                    
            signup_success_flag = 0
            signup_templ_params['error_first_name'] = "Invalid first name!"
        
        if not last_name_flag:                    
            signup_success_flag = 0
            signup_templ_params['error_last_name'] = "Invalid last name!"
        
        if not postal_address_flag:                    
            signup_success_flag = 0
            signup_templ_params['error_postal_address'] = "Invalid postal address!"
        
        if not restaurant_flag:
            signup_templ_params['error_restaraunt'] = "Invalid restaurant name!"
            signup_success_flag = 0
            

        if (signup_success_flag):                        
            corrd = get_geolocation(user_postal_address)             
            q = UserPass_Chef(user_id = userid,user_firstname = user_first_name,user_lastname = user_last_name,restaurant_name=restaraunt_val,
                user_address = user_postal_address,user_email=user_email,user_latitude = corrd[0],
                user_longitude=corrd[1],user_phone=userphone,user_bankacnt=user_paypal_email,no_reviews=0,user_rating=0)
            q.put()
            
            d = db.GqlQuery("SELECT * FROM UserPass_User WHERE user_id = '%s' " %userid)
            l = d.get()  
            l.ischef = 1
            l.user_firstname = user_first_name
            l.user_lastname = user_last_name
            l.user_address = user_postal_address
            l.user_latitude = corrd[0]
            l.user_longitude = corrd[1]
            l.user_phone = userphone
            l.user_email = user_email

            l.put()                                            
            
            self.redirect('/welcome')
        else:
            self.response.out.write(template.render('./html/signup_chef.html',signup_templ_params))