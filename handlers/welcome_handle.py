import webapp2

from utils import valid_hash_cookie
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from utils import *
from time import gmtime, strftime
from datetime import datetime

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        temp = self.request.cookies.get('user_id')
        if temp:
            userid = valid_hash_cookie(temp)
            if userid:
                dashboard_params = {}
                
                d = db.GqlQuery("SELECT * FROM UserPass_User WHERE user_id = '%s' " % userid)
                l = d.get()
                if l:
                    if (l.ischef):
                        chef_flag = 1
                    else:
                        chef_flag = 0
                else:
                    self.response.out.write('Error! No username!')
                    chef_flag = 0
                    
                dashboard_params['userid'] = userid
                dashboard_params['chef_flag'] = chef_flag
                dashboard_params['home_site'] = home_site
                
                #-----------------------Extract Past Few Orders---------------------
                d = db.GqlQuery("SELECT * FROM UserPass_User WHERE user_id = '%s' " % userid)
                l = d.get()
                orders_details_brief = []
                
                if l:
                    orders_list = l.orders                
                    for k in orders_list:
                        order = db.get(k)
                        if order:
                            srt = order.order_details
                    
                            str_temp = 'item_count'
                            em = re.search('%s=\S+'%str_temp, srt)                    
                            if em:
                                temp = em.group(0)
                                item_count = temp[11:len(temp)]
                                item_count = int(item_count)
                        
                            order_specifications = []
                            for i in range(1,item_count+1):
                                order_specifications = []
                                
                        
                                str_temp = 'item_name_'+str(i)
                                em = re.search('%s\S+'%str_temp, srt)                    
                                if em:
                                    temp = em.group(0)
                                    item_name = temp[11:len(temp)]
                                    order_specifications.append(item_name)
                        
                                str_temp = 'item_quantity_'+str(i)
                                em = re.search('%s\S+'%str_temp, srt)                    
                                if em:
                                    temp = em.group(0)
                                    item_quantity = temp[15:len(temp)]
                                    item_quantity = int(item_quantity)
                                    order_specifications.append(item_quantity)
                    
                                str_temp = 'item_chef_'+str(i)
                                em = re.search('%s\S+'%str_temp, srt)                    
                                if em:
                                    temp = em.group(0)
                                    item_chef = temp[11:len(temp)]                            
                                    order_specifications.append(item_chef)
                                
                                str_temp = 'item_delivery_'+str(i)
                                em = re.search('%s\S+'%str_temp, srt)                    
                                if em:
                                    temp = em.group(0)
                                    item_delivery = temp[15:len(temp)]                            
                                    item_delivery = item_delivery.replace('%3A',':')
                                    item_delivery = item_delivery.replace('%26','&')
                                    order_specifications.append(item_delivery)
                                

                                str_temp = 'item_price_'+str(i)
                                em = re.search('%s\S+'%str_temp, srt)                    
                                if em:
                                    temp = em.group(0)
                                    item_price = temp[12:len(temp)]
                                    item_price = float(item_price)
                                    order_specifications.append(item_price)
                        
                                str_temp = 'item_id_'+str(i)
                                em = re.search('%s\S+'%str_temp, srt)                    
                                if em:
                                    temp = em.group(0)
                                    item_id = temp[9:len(temp)]                            
                                    order_specifications.append(item_id)
                        
                            orders_details_brief.append(order_specifications)                                         
                    #------------------------------------------------------------------------
                        
                
                dashboard_params['orders_details_brief'] = orders_details_brief
                #----------------------------------------------------------------------------
                
                #-------------------------Add Recommendations--------------------------------
                search_results = []
                thismoment = datetime.now()
                thismoment = thismoment.replace(microsecond=0)
        
                rightnow = datetime.strptime(str(thismoment), "%Y-%m-%d %H:%M:%S")
                meal_query = "SELECT * FROM FoodList WHERE offered_date_begin < DATETIME('%s')" %rightnow
                meals_list = db.GqlQuery(meal_query)
                
                success_flag = 0
                food_counter = 0        
                for meal in meals_list:
                    chefs = db.GqlQuery("SELECT * FROM UserPass_Chef WHERE user_id = '%s'" %meal.chef_id)
                    chef = chefs.get()
                    if meal.offered_date_finish > rightnow:
                        if meal.meal_promotion_msg:
                            food_counter = food_counter + 1
                            review_specifications = []                    
                            review_specifications.append(unescape_html(meal.title))                            
                            review_specifications.append((meal.key()))
                            review_specifications.append(str(meal.chef_id))
                                        
                            rating_str = ""
                            
                            for i in range(int(chef.user_rating)):
                                rating_str = rating_str + "<span>&#9733</span>"
                            for i in range(5-int(chef.user_rating)):    
                                rating_str = rating_str + "<span>&#9734</span>"
                                        
                            review_specifications.append(rating_str)
                            search_results.append(review_specifications)
                            success_flag = 1
                        
                            if (food_counter>4):
                                break
                            
                if success_flag:
                    dashboard_params['food_list'] = search_results
                    
                self.response.out.write(template.render('./html/user_dashboard.html',dashboard_params))
                
            else:
                self.response.out.write('Cheater!')
        else:
            self.redirect('/login')
