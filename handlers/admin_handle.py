#=================================FUNCTION DESCRITION================================
# This file contains the necessary codes that are responsible for adding the food
# types and ingredients to the corresponding database.

# NOTE: the meal type and ingredients must be added one at a time
#====================================================================================


#=================INCLUDING THE NECESSARY LIBRARIES AND OTHER FILES==================
import webapp2
from google.appengine.ext.webapp import template
from utils import *
from google.appengine.ext import db
from dbs.databases import *
from google.appengine.api import memcache
from datetime import datetime
#====================================================================================


#===================================THE MAIN CODE====================================
class AdminHandler(webapp2.RequestHandler):
 
    
    #----------------------Display the Form Upon Loading the Page--------------------
    def get(self):
        params_new_post = {}        
        self.response.out.write(template.render('./html/add_ingredients.html',params_new_post))     # Display the html file
    #--------------------------------------------------------------------------------
    
    #------------------Get Admin's Inputs and Add The to the Database----------------        
    def post(self): 
        params_new_post = {}                                                    # The list of parametersthat will be passed to the html template
        meal_title = escape_html(self.request.get('food_name'))                 # Get the type of the meal from the admin
        ingredient_title = escape_html(self.request.get('ingredient_name'))     # Get the name of the ingredient from the admin
        
        success_flag = 0
        
        #---------------------Add the Meal Title to the Database---------------------
        if meal_title:
            a = FoodTitles(title = meal_title,food_type = '')
            a.put()
            success_flag = 1
        #----------------------------------------------------------------------------
        
        #------------------Add the Ingredient Title to the Database------------------
        if ingredient_title:
            a = IngredientsTitles(title = ingredient_title,ingredient_type = '')
            a.put()
            success_flag = 1
        #----------------------------------------------------------------------------
            
        if success_flag:            
            self.response.out.write('Success!')
        else:
            self.response.out.write('Failure!')    
    #--------------------------------------------------------------------------------        
            
#====================================================================================