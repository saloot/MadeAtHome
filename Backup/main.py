#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import random
import string
import hashlib
import datetime
import time
import Cookie
import json
import urllib2
import urllib


from handlers.login_handle import LoginHandler
from handlers.logout_handle import LogoutHandler
from handlers.newpost_handle import NewPostHandler
from handlers.displaypost_handle import DisplayPostHandler
from handlers.displaypost_handle import DisplayPostHandler_JSON
from handlers.signup_handle import SignUpHandler
from handlers.welcome_handle import WelcomeHandler
from handlers.chefprofile_handle import ChefProfileHandler
from handlers.displaymap_handle import DisplayMapHandler
from handlers.admin_handle import AdminHandler
from handlers.image_handle import ImageHandler
from handlers.review_handle import ReviewHandler
from utils import *

from time import gmtime, strftime
from datetime import datetime
from collections import namedtuple

from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from dbs.databases import *

inf = 100000

class MainHandler(webapp2.RequestHandler):
    def get(self):
        params_front = {}
        food_list = []
        
        thismoment = datetime.now()
        thismoment = thismoment.replace(microsecond=0)
        
        rightnow = datetime.strptime(str(thismoment), "%Y-%m-%d %H:%M:%S")
        
        datetime_val = str(thismoment)[0:10]+'T'+str(thismoment)[11:16]
        
        
        front_page = db.GqlQuery("SELECT * FROM FoodList WHERE offered_date > DATETIME('%s')" %rightnow)
        
        params_front['datetime_value'] = datetime_val
        
        counter = 0
        meals_list = []
        for meals in front_page:
            if meals.title.lower() not in meals_list:
                meals_list.append(meals.title.lower())
                counter = counter + 1
                
                meal_str = (meals.title)                
                
                
                food_list.append(meal_str)
                
            
        params_front['food_list'] = food_list
        params_front['isactive'] = "1"
        temp = self.request.cookies.get('user_id')
        if temp:
            userid = valid_hash_cookie(temp)
            if userid:
                params_front['userid'] = userid
        
        self.response.out.write(template.render('./html/front_page.html',params_front))
        
    def post(self):
        params_front = {}        
        search_results = []
        
        
        #delivery_address = self.request.get('delivery_address')
        selected_meals = (self.request.get_all('selected_meals'))
        #selected_meals = ",".join(selected_meals) 
        delivery_date = self.request.get('delivery_time')
        #max_price = (self.request.get('max_price'))
        #min_chef_rate = int(self.request.get('min_rate'))
        
        

        
        success_flag = 1
        
        
        #if not delivery_address:
        #    success_flag = 0
        #    params_front['error_delivery'] = 'Dude! we need your delivery address!'
        
        if not selected_meals:
            success_flag = 0
            params_front['error_meals'] = 'Dude! if you wanna eat, you should select something!'
        else:
            selected_meals = (selected_meals)
            
        #if not max_price:
        max_price = inf
        #else:
        #    max_price = int(max_price)
        #    params_front['price_value'] = max_price                
        
        if not delivery_date:
            success_flag = 0
            params_front['error_date'] = 'Dude! when do you want to eat?!'
        else:
            params_front['datetime_value'] = delivery_date
            
        #params_front['delivery_value'] = delivery_address
        
        if not success_flag:
            thismoment = datetime.now()
            thismoment = thismoment.replace(microsecond=0)  
        
            rightnow = datetime.strptime(str(thismoment), "%Y-%m-%d %H:%M:%S")
            front_page = db.GqlQuery("SELECT * FROM FoodList WHERE offered_date > DATETIME('%s')" %rightnow)
            
            #food_list = []
            #counter = 0
            #search_results = []
            #for meals in front_page:
            #    if meals.title.lower() not in meals_list:
            #        meals_list.append(meals.title.lower())
            #        counter = counter + 1
            #        meal_str = str(meals.title)
            #        food_list.append(meal_str)
                
            
            #params_front['food_list'] = food_list
            self.response.out.write(template.render('./html/front_page.html',params_front))
        else:
            delivery_date = datetime.strptime(str(delivery_date), "%Y-%m-%dT%H:%M")
            meal_query = "SELECT * FROM FoodList WHERE offered_date > DATETIME('%s')" %delivery_date
            
            meals_list = db.GqlQuery(meal_query)
            if meals_list is not None:
                
                success_flag = 0
                for meal in meals_list:
                    
                #    if meal.price <= max_price:
                #        success_flag_temp = 1
                        
                #        if not min_chef_rate:
                #            min_chef_rate = 0
                            
                    chefs = db.GqlQuery("SELECT * FROM UserPass_Chef WHERE user_id = '%s'" %meal.chef_id)
                    chef = chefs.get()
                            
                #        if chef.user_rating < min_chef_rate:
                #            success_flag_temp = 0
                        
                    
                #        if success_flag_temp:
                #            success_flag_temp = 0
                    
                    for desired_title in selected_meals:                        
                        if meal.meal_type == str(desired_title):
                            
                            meal_specifications = []                    
                            meal_specifications.append(unescape_html(meal.title))
                            meal_specifications.append(int(meal.price))
                            meal_specifications.append(int(meal.max_quantity))                                    
                            meal_specifications.append((meal.offered_date))
                            meal_specifications.append((meal.key()))
                            meal_specifications.append(str(meal.chef_id))
                                    
                            rating_str = ""
                            
                            for i in range(int(chef.user_rating)):
                                rating_str = rating_str + "<span>&#9733</span>"
                            for i in range(5-int(chef.user_rating)):    
                                rating_str = rating_str + "<span>&#9734</span>"
                                        
                            meal_specifications.append(rating_str)
                            search_results.append(meal_specifications)
                            success_flag = 1
                            break
                            
                if not success_flag:
                    self.response.out.write('Sorry your query did not yield any results!')
                else:
                    params_front['food_list'] = search_results
                    params_front['isactive'] = "1"
                    temp = self.request.cookies.get('user_id')
                    if temp:
                        userid = valid_hash_cookie(temp)
                        if userid:
                            params_front['userid'] = userid
                    self.response.out.write(template.render('./html/display_search_results.html',params_front))        
            else:
                self.response.out.write('Sorry your query did not yield any results!')
                        
                    

                     
                    
                    
            
        
        

class MainHandler_JSON(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        posts = db.GqlQuery("SELECT * FROM Blogpost ORDER BY created_date DESC")        
        post_dictionary = []
        for blog_post in posts:
            post_dictionary.append(print_json(self,blog_post))
                    
        self.response.out.write(json.dumps(post_dictionary))
            
        key = 'front'
        front_page = memcache.get(key)
        if front_page is None:
            front_page = db.GqlQuery("SELECT * FROM Blogpost ORDER BY created_date DESC LIMIT 10")
            front_page = list(front_page)
            memcache.set(key,front_page)
            memcache.set('time',time.time())

        for blog_post in front_page:            
            self.response.write('<h1>%s</h1>'%blog_post.title)
            self.response.write('<br>')
            self.response.write(blog_post.content)
            self.response.write('<br>')
            self.response.write('<hr>')
        last_chached = memcache.get('time')
        if last_chached:
            self.response.write('Queried %f seconds ago' %(time.time()-last_chached))

        
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/.json/?', MainHandler_JSON),    
    ('/_admin/?', AdminHandler),
    ('/_image', ImageHandler),
    ('/signup/?', SignUpHandler),
    ('/_chef/?', ChefProfileHandler),
    ('/newpost/?', NewPostHandler),
    ('/welcome/?', WelcomeHandler),
    ('/login/?', LoginHandler),
    ('/logout/?', LogoutHandler),
    ('/display_map/?', DisplayMapHandler),    
    ('/_meal', DisplayPostHandler),
    ('/_rev', ReviewHandler),
    ('/([a-zA-Z0-9]+.json)/?', DisplayPostHandler_JSON)
], debug=True)
