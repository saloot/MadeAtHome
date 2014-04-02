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
from utils import *

from time import gmtime, strftime
from datetime import datetime
from collections import namedtuple

from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from dbs.databases import *

inf = 100000

class SearchHandler(webapp2.RequestHandler):
    
    def get(self):
        
        params_front = {}        
        search_results = []
        search_results_sorted_price = []
        
        selected_meals = unescape_html(self.request.get('u'))
        delivery_date = unescape_html(self.request.get('v'))
        hashed_val = escape_html(self.request.get('v'))
        hashed_val.replace('&nbsp','aa')
        hashed_val.replace('%20','aa')
        
        self.response.headers.add_header('Set-Cookie','delivery_date=%s' % str(hashed_val))
        
        sort_option = unescape_html(self.request.get('s'))
        base_query = '?u=%s&v=%s' %(selected_meals,delivery_date)
        selected_meals= selected_meals.split(',')
        meal_query = "SELECT * FROM FoodList WHERE offered_date_begin < DATETIME('%s')" %delivery_date
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
                        if datetime.strptime(str(delivery_date), "%Y-%m-%d %H:%M:%S") < meal.offered_date_finish:
                            review_specifications = []                    
                            review_specifications.append(unescape_html(meal.title))
                            review_specifications.append(int(meal.price))
                            review_specifications.append(int(meal.max_quantity))                                    
                            review_specifications.append((meal.offered_date_begin.date()))
                            review_specifications.append((meal.key()))
                            review_specifications.append(str(meal.chef_id))
                            
                            rating_str = ""
                                
                            for i in range(int(chef.user_rating)):
                                rating_str = rating_str + "<span>&#9733</span>"
                            for i in range(5-int(chef.user_rating)):    
                                rating_str = rating_str + "<span>&#9734</span>"
                                            
                            review_specifications.append(rating_str)
                            review_specifications.append((meal.offered_date_finish.date()))
                            search_results.append(review_specifications)
                            success_flag = 1
                            break
                            
            if not success_flag:
                self.response.out.write('Sorry your query did not yield any results!')
            else:
                search_results_sorted_price = sorted(search_results,key=lambda student: student[1])
                search_results_sorted_date = sorted(search_results,key=lambda student: student[3])
                search_results_sorted_rate = sorted(search_results,key=lambda student: student[6])
                if (sort_option == 'normal'):
                    params_front['food_list'] = search_results
                elif (sort_option == 'price'):
                    params_front['food_list'] = search_results_sorted_price
                elif (sort_option == 'date'):
                    params_front['food_list'] = search_results_sorted_date
                elif (sort_option == 'rate'):
                    params_front['food_list'] = search_results_sorted_rate
                else:
                    params_front['food_list'] = search_results
                    
                params_front['base_query'] = base_query
                params_front['isactive'] = "1"
                temp = self.request.cookies.get('user_id')
                if temp:
                    userid = valid_hash_cookie(temp)
                    if userid:
                        params_front['userid'] = userid
                        user = db.GqlQuery("SELECT * FROM UserPass_User WHERE user_id = '%s'" %userid)
                        user = user.get()
                        params_front['chef_flag'] = user.ischef
                
                
                #---------------------------Detect the Location From IP-------------------
                ip = self.request.remote_addr
                response = urllib.urlopen('http://api.hostip.info/get_html.php?ip=%s&position=true'%ip).read()
        
                em = re.search('Longitude: \S+', str(response))
                if em:
                    temp = em.group(0)
                    user_long = temp[10:len(temp)]            
                else:
                    user_long = ''
        
                em = re.search('Latitude: \S+', str(response))
                if em:
                    temp = em.group(0)
                    user_lat = temp[10:len(temp)]
                    self.response.out.write(user_lat)
                else:
                    user_lat = ''
            
                em = re.search('Country: \S+', str(response))
                if em:
                    temp = em.group(0)
                    user_country = temp[9:len(temp)]
                    if user_country != '(Private': 
                        user_address = user_country
                    else:
                        user_address = 'Unknown'
                    
                else:
                    user_country = ''
        
                em = re.search('City: \S+', str(response))
                if em:
                    temp = em.group(0)
                    user_city = temp[6:len(temp)]
                    if ( (user_city != '(Unknown') & (user_city != '(Private')): 
                        user_address = user_address + ', ' + user_city
                else:
                    user_city = ''
                    
                
                params_front['user_address'] = user_address
                #-------------------------------------------------------------------------
        
                #------------------------Extract Delivery Date----------------------------
                month = delivery_date[5:7]
                if (month == '01'):
                    month = 'January'
                elif (month == '02'):
                    month = 'February'
                elif (month == '03'):
                    month = 'March'
                elif (month == '04'):
                    month = 'April'
                elif (month == '05'):
                    month = 'May'
                elif (month == '06'):
                    month = 'June'
                elif (month == '07'):
                    month = 'July'
                elif (month == '08'):
                    month = 'August'
                elif (month == '09'):
                    month = 'September'
                elif (month == '10'):
                    month = 'October'
                elif (month == '11'):
                    month = 'November'
                else:
                    month = 'December'
                
                deliv_hour = delivery_date[11:13]
                deliv_time = delivery_date[11:16]
                deliv_date = delivery_date[8:10] + ' ' + month + ', ' + delivery_date[0:4]
                
                if (int(deliv_hour) >= 12):
                    deliv_date = deliv_date + ' at ' + deliv_time + ' PM'
                else:
                    deliv_date = deliv_date + ' at ' + deliv_time + ' AM'
                #self.response.out.write(deliv_date)
                params_front['delivery_date'] = deliv_date
                #-------------------------------------------------------------------------
                
                self.response.out.write(template.render('./html/display_search_results.html',params_front))        
        else:
            self.response.out.write('Sorry your query did not yield any results!')
                        
                    
                    

                     
    