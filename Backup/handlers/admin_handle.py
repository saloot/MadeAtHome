import webapp2
from google.appengine.ext.webapp import template
from utils import *
from google.appengine.ext import db
from dbs.databases import *
from google.appengine.api import memcache
from datetime import datetime

class AdminHandler(webapp2.RequestHandler):
    
    def get(self):
        params_new_post = {}        
        self.response.out.write(template.render('./html/add_ingredients.html',params_new_post))
        
    def post(self): 
        params_new_post = {}  
        meal_title = escape_html(self.request.get('food_name'))
        ingredient_title = escape_html(self.request.get('ingredient_name'))
        
        success_flag = 0
        
        if meal_title:
            a = FoodTitles(title = meal_title,food_type = '')
            a.put()
            success_flag = 1
        
        if ingredient_title:
            a = IngredientsTitles(title = ingredient_title,ingredient_type = '')
            a.put()
            success_flag = 1
            
        if success_flag:            
            self.response.out.write('Success!')
        else:
            self.response.out.write('Failure!')
