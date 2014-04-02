#=================================FUNCTION DESCRITION================================
# The code in this file handles the chefs signup process. It displays the signup form,
# gets the user's input, process them and if all necessary fields were complete and
# consistent with the requirements, it adds the inserted information to the
# corresponding database.
#====================================================================================


#=================INCLUDING THE NECESSARY LIBRARIES AND OTHER FILES==================
import webapp2
from madeathome_forms import form_login
from utils import *
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from dbs.databases import UserPass_Chef
from dbs.databases import UserPass_User 
#====================================================================================


#===================================THE MAIN CODE====================================
class ChefSignUpHandler(webapp2.RequestHandler):               
     
    #----------------------Display the Form Upon Loading the Page--------------------    
    def get(self):
        
        signup_templ_params = {}                                # The list of parametersthat will be passed to the html template
        temp = self.request.cookies.get('user_id')              # Check if the user has signed in
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
    #--------------------------------------------------------------------------------             

    #-----------------------Get User's Input and Process Them------------------------
    def post(self):
        signup_templ_params = {}                                    # The list of parametersthat will be passed to the html template
        
        #-----------------------Check If the User has Signed In----------------------        
        temp = self.request.cookies.get('user_id')                  # Read the cookies that specify if a user has signed in
        if temp:
            userid = valid_hash_cookie(temp)
            if userid:
                signup_templ_params['userid'] = userid
            else:
                self.response.out.write('what the hell? invlaid user?!')
        else:
            self.response.out.write('what the hell? no user?!')
        #----------------------------------------------------------------------------
        
        #-------------------------Get User's Inputs----------------------------------
        user_first_name = self.request.get('first_name')            # The first name of the user
        user_last_name = self.request.get('last_name')              # The last name of the user
        user_postal_address = self.request.get('postal_address')    # The postal address of the user
        restaraunt_val = self.request.get('restaraunt')             # The name of the user's restaurant
        user_email = self.request.get('email')                      # The email of the user
        user_paypal_email = self.request.get('paypl')               # The paypal address of the user
        userphone = str(self.request.get('cellphone'))              # The user's phone number 
        #----------------------------------------------------------------------------
        
        #-Assign HTML Template Parameters in Case we Have to Reload the Signup Page--
        signup_templ_params['first_name_value']= str(user_first_name)
        signup_templ_params['last_name_value']= str(user_last_name)
        signup_templ_params['postal_address_value'] = str(user_postal_address)
        signup_templ_params['paypal_email'] = str(user_paypal_email)
        signup_templ_params['cell_phone'] = str(userphone)
        signup_templ_params['restaraunt_value'] = restaraunt_val
        #----------------------------------------------------------------------------
        
        #-----------------Check the Validity of Inserted Information-----------------
        first_name_flag = valid_name(user_first_name)               # Check if the first name is valid
        last_name_flag = valid_name(user_last_name)                 # Check if the last name is valid 
        restaurant_flag = valid_name(restaraunt_val)                # Check if the restaurant is valid
        postal_address_flag = valid_address(user_postal_address)    # Check if the postal address is valid   
        signup_success_flag = 1
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
        #----------------------------------------------------------------------------
        
        
        #---------If Everything was Valid, Insert the Info into the Database---------
        if (signup_success_flag):                        
            corrd = get_geolocation(user_postal_address)            
            q = UserPass_Chef(user_id = userid,user_firstname = user_first_name,user_lastname = user_last_name,restaurant_name=restaraunt_val,
                user_address = user_postal_address,user_email=user_email,user_latitude = corrd[0],
                user_longitude=corrd[1],user_phone=userphone,user_bankacnt=user_paypal_email,no_reviews=0,user_rating=0)
            #q = UserPass_Chef(user_id = userid,user_firstname = user_first_name,user_lastname = user_last_name,restaurant_name=restaraunt_val,
            #    user_address = user_postal_address,user_email=user_email,user_latitude = '0',
            #    user_longitude='0',user_phone=userphone,user_bankacnt=user_paypal_email,no_reviews=0,user_rating=0)
            q.put()
            
            d = db.GqlQuery("SELECT * FROM UserPass_User WHERE user_id = '%s' " %userid)
            l = d.get()  
            l.ischef = 1
            l.user_firstname = user_first_name
            l.user_lastname = user_last_name
            l.user_address = user_postal_address
            l.user_latitude = corrd[0]
            l.user_longitude = corrd[1]
            #l.user_latitude = '0'
            #l.user_longitude = '1'
            l.user_phone = userphone
            l.user_email = user_email

            l.put()                                            
            
            
            self.redirect('/welcome')                                       # Redirect the user to the welcome page
        #----------------------------------------------------------------------------    
            
        #-------Otherwise, Reload the Signup Page with Proper Error Messages---------
        else:
            self.response.out.write(template.render('./html/signup_chef.html',signup_templ_params))
        #----------------------------------------------------------------------------
        
    #--------------------------------------------------------------------------------
#====================================================================================