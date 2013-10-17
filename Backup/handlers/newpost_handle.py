import webapp2
from google.appengine.ext.webapp import template
from google.appengine.api import images
from utils import *
from google.appengine.ext import db
#from dbs.databases import FoodList
#from dbs.databases import UserPass_Chef
from dbs.databases import *
from google.appengine.api import memcache
from datetime import datetime
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images

class NewPostHandler(webapp2.RequestHandler):
    
    def get(self):
        params_new_post = {}
        
        thismoment = datetime.now()
        thismoment = thismoment.replace(microsecond=0)    
        datetime_val = str(thismoment)[0:10]+'T'+str(thismoment)[11:16]
        params_new_post['date_of_meal'] = datetime_val
        
        ingredients_list = []
        ingredients_db = db.GqlQuery("SELECT * FROM IngredientsTitles")        
        if ingredients_db:            
            for ingredient in ingredients_db:
                ingredients_list.append(str(ingredient.title))
                
        params_new_post['ingredients_list'] = ingredients_list
        
        food_types_list = []
        food_db = db.GqlQuery("SELECT * FROM FoodTitles")        
        if food_db:            
            for food in food_db:
                food_types_list.append(food.title)
        
        temp = self.request.cookies.get('user_id')
        if temp:
            userid = valid_hash_cookie(temp)
            if userid:
                params_new_post['userid'] = userid
        params_new_post['food_types_list'] = food_types_list
        params_new_post['isactive'] = ["active","0","0"]
        
        self.response.out.write(template.render('./html/new_post.html',params_new_post))
        
    def post(self): 
        params_new_post = {}  
        meal_title = escape_html(self.request.get('meal_desired_title'))
        type_of_meal = str(escape_html(self.request.get('meal_type')))
        meal_quantity = self.request.get('meal_quantity')
        meal_date = self.request.get('meal_date')
        meal_price = (self.request.get('meal_price'))
        image1 = str(self.request.get('food_img1'))
        image1 = db.Blob(image1)
        image2 = str(self.request.get('food_img2'))
        image2 = db.Blob(image2)
        image3 = str(self.request.get('food_img3'))
        image3 = db.Blob(image3)
        image4 = str(self.request.get('food_img4'))
        image4 = db.Blob(image4)
        meal_description = escape_html(self.request.get('description_of_meal'))
        #image2 = db.Blob(str(self.request.get('food_img2')))
        #image3 = db.Blob(str(self.request.get('food_img3')))
        #image4 = db.Blob(str(self.request.get('food_img4')))
        image5 = db.Blob(str(self.request.get('food_img5')))
  
        
        success_flag = 1
                
        
        meal_ingredients_list = (self.request.get_all('meal_ingredients'))
        
        ingredients_list = []
        ingredients_db = db.GqlQuery("SELECT * FROM IngredientsTitles")        
        if ingredients_db:            
            for ingredient in ingredients_db:
                ingredients_list.append(str(ingredient.title))
                
        params_new_post['ingredients_list'] = ingredients_list
        
        food_types_list = []
        food_db = db.GqlQuery("SELECT * FROM FoodTitles")        
        if food_db:            
            for food in food_db:
                food_types_list.append(food.title)
        
        params_new_post['food_types_list'] = food_types_list
        params_new_post['description_meal'] = meal_description
        params_new_post['customized_meal_title'] = meal_title
        
        if not meal_title:
            params_new_post['error_title'] = "Title is necessary!"
            params_new_post['title_of_meal'] = ''
            success_flag = 0
        else:
            params_new_post['title_of_meal'] = meal_title
            
        if not meal_ingredients_list:
            success_flag = 0
            params_new_post['error_ingredients'] = "Ingredients are necessary!"
            params_new_post['ingredients_of_meal'] = ''
        else:
            params_new_post['ingredients_of_meal'] = meal_ingredients_list            
        
        if not meal_date:
            params_new_post['error_date'] = "Date is necessary!"
            params_new_post['date_of_meal'] = ''
            success_flag = 0
        else:
            meal_date_pyth = datetime.strptime(meal_date, "%Y-%m-%dT%H:%M")
            params_new_post['date_of_meal'] = meal_date
            
        if not meal_quantity:
            params_new_post['error_quantity'] = "Quantity is necessary!"
            params_new_post['quantity_of_meal'] = ''
            success_flag = 0
        else:
            params_new_post['quantity_of_meal'] = meal_quantity
            
        if not meal_price:
            params_new_post['error_price'] = "Price is necessary!"
            params_new_post['price_of_meal'] = ''
            success_flag = 0
        else:
            meal_price = int(meal_price)
            params_new_post['price_of_meal'] = meal_price
        if not (image1):
            params_new_post['error_image'] = 'You should submit at least one picture!'
            success_flag = 0
        
        if not meal_description:
            params_new_post['error_description'] = 'Due you should write something to describe the fucking meal!!'
            success_flag = 0
            
        if not success_flag:            
            self.response.out.write(template.render('./html/new_post.html',params_new_post))
        else:
            temp = self.request.cookies.get('user_id')
            if temp:
                chef_id = valid_hash_cookie(temp)
                if not chef_id:
                    self.redirect('/login')
            else:
                self.redirect('/login')        
            
            u = db.GqlQuery("SELECT * FROM UserPass_Chef WHERE user_id = '%s'" %chef_id)
            chef = u.get()
            
            b = FoodList(title = meal_title,ingredients = meal_ingredients_list,created_date = datetime.now(),
                         offered_date = meal_date_pyth,chef_id = chef_id,max_quantity = int(meal_quantity),
                         chef_firstname = chef.user_firstname,chef_lastname = chef.user_lastname,
                         chef_address = chef.user_address,chef_email = chef.user_email,chef_phone = chef.user_phone,
                         chef_latitude = chef.user_latitude,chef_longitude = chef.user_longitude,
                         chef_bankacnt = chef.user_bankacnt, price = meal_price, food_image1 = image1,
                         food_image2 = image2,food_image3 = image3,food_image4 = image4,food_image5 = image5, description = meal_description, meal_type = type_of_meal)
            b.put()
            d = db.GqlQuery("SELECT * FROM FoodList WHERE title = '%s'" %meal_title)
            l = d.get()
            
            #front_page = db.GqlQuery("SELECT * FROM FoodList ORDER BY created_date DESC LIMIT 10")
            #front_page = list(front_page)
            #memcache.set('front',front_page)
            #memcache.set('time',time.time())
            
            perma_link=('./_meal?m=%s' %str(b.key()))
            
            self.redirect('/%s' %perma_link)
