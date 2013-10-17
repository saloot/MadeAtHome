import webapp2
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from dbs.databases import *
from utils import *
import time

class ChefProfileHandler(webapp2.RequestHandler):
    def get(self):
        params_profile = {}        
        meals_list = []
        meals_price_list = []
        
        temp = self.request.cookies.get('user_id')
        if temp:
            userid = valid_hash_cookie(temp)
            if userid:
                params_profile['userid'] = userid
        
        u = self.request.get('u')
        chef = db.GqlQuery("SELECT * FROM UserPass_Chef WHERE user_id = '%s'" %u)
        if not chef:
            self.response.out.write('Invalid Chef ID!')
        else:            
            chef = chef.get()
            
            params_profile['chef_name'] = chef.user_firstname + ' ' + chef.user_lastname
            
            rating_str = ""             
            for i in range(int(chef.user_rating)):
                rating_str = rating_str + "<span>&#9733</span>"
            for i in range(5-int(chef.user_rating)):
                rating_str = rating_str + "<span>&#9734</span>"
             
                                        
            params_profile['chef_rating'] = rating_str               
            params_profile['no_reviews'] = chef.no_reviews
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
                
            
        params_profile['food_list'] = meals_list 
        
        params_profile['chef_id'] = chef.user_id
        
        self.response.out.write(template.render('./html/display_profile.html',params_profile))
            