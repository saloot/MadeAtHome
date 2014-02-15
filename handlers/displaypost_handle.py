#=================================FUNCTION DESCRITION================================
# This code is responsible for displaying a particular meal. It reads the meal ID
# from the url, retrieves the meal from the dataset and if found, displays its
# detaiLs.
#====================================================================================


#=================INCLUDING THE NECESSARY LIBRARIES AND OTHER FILES==================
import webapp2
from google.appengine.api import memcache
from google.appengine.ext import db
import time
from dbs.databases import *
from utils import *
from google.appengine.ext.webapp import template
from datetime import date
#====================================================================================

#===================================THE MAIN CODE====================================
class DisplayPostHandler(webapp2.RequestHandler):

    def get(self):   
        meal_key = self.request.get('m')
        key = 'post_%s' %meal_key
        
        temp = self.request.cookies.get('delivery_date')
        if temp:
            delivery_date = temp
        else:
            thismoment = datetime.now()
            thismoment = thismoment.replace(microsecond=0)
        
            rightnow = datetime.strptime(str(thismoment), "%Y-%m-%d %H:%M:%S")
        
            datetime_val = str(thismoment)[0:10]+'T'+str(thismoment)[11:16]
            delivery_date = rightnow
        #key_time = 'time_post_%s' %meal_key
        #meal = memcache.get(key)        
        #if meal is None:            
        #    meal = db.get(meal_key) 
        #    #meals = db.GqlQuery("SELECT * FROM FoodList WHERE title = '%s'" %meal_key)
        #    #meal = meals.get()                                                
        #    memcache.set(key,meal)
        #    memcache.set(key_time,time.time())    
            
        meal = db.get(meal_key) 
        food = []                    
        food.append(unescape_html(meal.title))
        food.append(int(meal.price))
        food.append(int(meal.max_quantity))
        food.append(meal.offered_date_begin.date())
        food.append(meal.offered_date_finish.date())
        food.append(meal.meal_type)
        
        params_profile = {}
        params_profile['chef_name'] = meal.chef_id
        params_profile['key'] = meal_key
        params_profile['food'] = food
        params_profile['food_description'] = unescape_html(meal.description)
        params_profile['delivery_time'] = delivery_date
        
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
                user = db.GqlQuery("SELECT * FROM UserPass_User WHERE user_id = '%s'" %userid)
                user = user.get()
                params_profile['chef_flag'] = user.ischef
                
        self.response.out.write(template.render('./html/display_post.html',params_profile))
                
        #last_chached = memcache.get(key_time)
        #if last_chached:
        #    self.response.write('Queried %f seconds ago' %(time.time()-last_chached))

#===============================THE JASON HANDLER====================================
# The JSON handler is responsible for producing proper JSON values, necessary for RSS
# feeds, APIs and so on.

class DisplayPostHandler_JSON(webapp2.RequestHandler):
    def get(self,meal_key):             
        q = db.GqlQuery("SELECT * FROM FoodList ORDER BY created_date DESC")
        meal = q.get()
        self.response.headers['Content-Type'] = 'application/json'
        
        post_dictionary = print_json(self,meal)
        self.response.out.write(json.dumps(post_dictionary))
#====================================================================================

