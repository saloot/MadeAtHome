#=================================FUNCTION DESCRITION================================
# This code is responsible for displaying the chefs' profiles, namely, all the food
# they offer, their favourite recipes, their rating, etc.
#====================================================================================


#=================INCLUDING THE NECESSARY LIBRARIES AND OTHER FILES==================
import webapp2
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from dbs.databases import *
from utils import *
import time
#====================================================================================


#===================================THE MAIN CODE====================================
class ChefProfileHandler(webapp2.RequestHandler):
    
    #---------------------Display the HTML Template Upon Loading---------------------    
    def get(self):
        
        params_profile = {}                         # The list of parametersthat will be passed to the html template
        
        #----------------------Check If a User Has Signed In-------------------------
        temp = self.request.cookies.get('user_id')
        if temp:
            userid = valid_hash_cookie(temp)
            if userid:
                params_profile['userid'] = userid
        #----------------------------------------------------------------------------
        
        #-----------------------Get the Chef ID From the URL-------------------------
        u = self.request.get('u')
        chef = db.GqlQuery("SELECT * FROM UserPass_Chef WHERE user_id = '%s'" %u)
        chef = chef.get()
        if not chef:
            self.redirect('/404?u=chef')
        #----------------------------------------------------------------------------    
        
        #--------------------------If the Chef ID Is Correct-------------------------
        else:            

            #------------------------Chef's Complete Name----------------------------
            params_profile['chef_name'] = chef.user_firstname + ' ' + chef.user_lastname
            #------------------------------------------------------------------------
            
            #-----------------------Extract Chef's Rating----------------------------
            rating_str = ""             
            for i in range(int(chef.user_rating)):
                rating_str = rating_str + "<span>&#9733</span>"
            for i in range(5-int(chef.user_rating)):
                rating_str = rating_str + "<span>&#9734</span>"
            #------------------------------------------------------------------------ 
                                        
            #-------------------Find the Meals Offerd by the Chef--------------------
            meals_list = []                             # The list of meals offered by the chef
            chef_meals = db.GqlQuery("SELECT * FROM FoodList WHERE chef_id = '%s'" %u)
            if chef_meals:                
                for meal in chef_meals:
                    meal_specifications = []                    
                    meal_specifications.append(unescape_html(meal.title))
                    meal_specifications.append(int(meal.price))
                    meal_specifications.append(int(meal.max_quantity))                    
                    meal_specifications.append((meal.offered_date))
                    meal_specifications.append((meal.key()))
                    meals_list.append(meal_specifications)
            #------------------------------------------------------------------------
            
            #-------------------Assign the HTML Template Parameters------------------
            params_profile['food_list'] = meals_list 
            params_profile['chef_rating'] = rating_str               
            params_profile['no_reviews'] = chef.no_reviews
            params_profile['chef_id'] = chef.user_id
            #------------------------------------------------------------------------
            
            #----------------------Display the Final HTML File-----------------------
            self.response.out.write(template.render('./html/display_profile.html',params_profile))
            #------------------------------------------------------------------------
            
        #----------------------------------------------------------------------------        
            
        
    #--------------------------------------------------------------------------------

#====================================================================================