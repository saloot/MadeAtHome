import webapp2
from google.appengine.api import memcache
from google.appengine.ext import db
import time
from dbs.databases import *
from utils import *
from google.appengine.ext.webapp import template

class DisplayPostHandler(webapp2.RequestHandler):
    def get(self):   
        meal_key = self.request.get('m')
        key = 'post_%s' %meal_key
        key_time = 'time_post_%s' %meal_key
        meal = memcache.get(key)
        if meal is None:            
            meal = db.get(meal_key) 
            #meals = db.GqlQuery("SELECT * FROM FoodList WHERE title = '%s'" %meal_key)
            #meal = meals.get()                                                
            memcache.set(key,meal)
            memcache.set(key_time,time.time())    
            
        
        food = []                    
        food.append(unescape_html(meal.title))
        food.append(int(meal.price))
        food.append(int(meal.max_quantity))                    
        food.append((meal.offered_date))
        
        
        params_profile = {}
        params_profile['chef_name'] = meal.chef_id
        params_profile['key'] = meal_key
        params_profile['food'] = food
        params_profile['food_description'] = unescape_html(meal.description)
        
        chefs = db.GqlQuery("SELECT * FROM UserPass_Chef WHERE user_id = '%s'" %meal.chef_id)
        chef = chefs.get()
        
        rating_str = ""
        for i in range(int(chef.user_rating)):
            rating_str = rating_str + "<span>&#9733</span>"
        for i in range(5-int(chef.user_rating)):    
            rating_str = rating_str + "<span>&#9734</span>"                            
            
        params_profile['chef_rate']= rating_str
                
        img_no_list = []
        if meal.food_image1:
            img_no_list.append(1)
        if meal.food_image2:
            img_no_list.append(2)
        if meal.food_image3:
            img_no_list.append(3)
        if meal.food_image4:
            img_no_list.append(4)
        if meal.food_image5:
            img_no_list.append(5)    
        params_profile['img_number_list'] = img_no_list
        
        params_profile['meal_left'] = meal.max_quantity
        params_profile['isactive'] = "1"
        temp = self.request.cookies.get('user_id')
        if temp:
            userid = valid_hash_cookie(temp)
            if userid:
                params_profile['userid'] = userid
        self.response.out.write(template.render('./html/display_post.html',params_profile))
                
        last_chached = memcache.get(key_time)
        #if last_chached:
        #    self.response.write('Queried %f seconds ago' %(time.time()-last_chached))

class DisplayPostHandler_JSON(webapp2.RequestHandler):
    def get(self,meal_key):             
        q = db.GqlQuery("SELECT * FROM FoodList ORDER BY created_date DESC")
        meal = q.get()
        self.response.headers['Content-Type'] = 'application/json'
        
        post_dictionary = print_json(self,meal)
        self.response.out.write(json.dumps(post_dictionary))


