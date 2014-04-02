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

import urllib

from time import gmtime, strftime
from datetime import date
from datetime import datetime
from collections import namedtuple
from google.appengine.api import mail
from google.appengine.api import taskqueue
#====================================================================================

#===================================THE MAIN CODE====================================
class PaymentHandler(webapp2.RequestHandler):

    def get(self):
        params_new_post = {}    
        temp = self.request.cookies.get('user_id')
        if temp:
            userid = valid_hash_cookie(temp)
            if userid:
                params_new_post['userid'] = userid
                user = db.GqlQuery("SELECT * FROM UserPass_User WHERE user_id = '%s'" %userid)
                user = user.get()
                params_new_post['chef_flag'] = user.ischef
        else:
            userid = []
                
        transaction_ID = self.request.get('tx')
        token = "KUZv42_xX9WzrpPT-kBbgib7LUwLSi2UtrNo-dc3awSYpKCPGDoEstm77YG"
        url = "https://www.sandbox.paypal.com/cgi-bin/webscr/cmd=_notify-synch&tx=" + transaction_ID
        url = url + "&at="
        url = url + token
        confirmPostRequest = urllib.urlopen(url,transaction_ID)
        response_str = confirmPostRequest.read()
        #self.response.out.write(response_str)
        
        #=====================EXTRACT PAYMENT DETAILS==================
        if re.search('^SUCCESS', response_str):
            em = re.search('(payer_email=)\S+', response_str)            
            if em:
                temp = em.group(0)
                user_email_add = temp[12:len(temp)]
                user_email_add  = user_email_add.replace("%40","@")
                #self.response.out.write(user_email_add)
            
            em = re.search('(business=)\S+', response_str)
            if em:
                temp = em.group(0)
                merchant_email_add = temp[9:len(temp)]
                merchant_email_add  = merchant_email_add.replace("%40","@")
                #self.response.out.write(merchant_email_add)
            
            em = re.search('(mc_gross=)\S+', response_str)
            if em:
                temp = em.group(0)
                payment_amount = float(temp[9:len(temp)])
                #self.response.out.write(payment_amount)
            
            em = re.search('(mc_shipping=)\S+', response_str)
            if em:
                temp = em.group(0)
                shipping_amount = temp[12:len(temp)]
                #self.response.out.write(shipping_amount)            
                
            em = re.search('(payment_status=)\S+', response_str)
            if em:
                temp = em.group(0)
                payment_status = temp[15:len(temp)]
                payment_status  = payment_status.replace("+"," ")
                #self.response.out.write(payment_status)
                
            user_address = ""
            em = re.search('(address_street=)\S+', response_str)
            if em:
                temp = em.group(0)
                delivery_address = temp[15:len(temp)]
                delivery_address  = delivery_address.replace("+"," ")
                #self.response.out.write(delivery_address)
                user_address = user_address + delivery_address
                
            em = re.search('(address_city=)\S+', response_str)
            if em:
                temp = em.group(0)
                delivery_city = temp[13:len(temp)]
                delivery_city  = delivery_city.replace("+"," ")
                #self.response.out.write(delivery_city)
                user_address = user_address + ", " + delivery_city
                
            em = re.search('(address_zip=)\S+', response_str)
            if em:
                temp = em.group(0)
                delivery_zip = temp[12:len(temp)]
                delivery_zip  = delivery_zip.replace("+"," ")
                #self.response.out.write(delivery_zip)
                user_address = user_address + ", " + delivery_zip
                
            em = re.search('(address_country=)\S+', response_str)
            if em:
                temp = em.group(0)
                delivery_country = temp[16:len(temp)]
                delivery_country  = delivery_country.replace("+"," ")
                #self.response.out.write(delivery_country)
                user_address = user_address + ", " + delivery_country
            
            em = re.search('(num_cart_items=)\d+', response_str)
            if em:
                temp = em.group(0)
                item_count = temp[15:len(temp)]                
                #self.response.out.write(item_count)            
            
            #-------------Detect Each Item on The Shopping Cart----------------
            items_lst = []
            order_description = "item_count=" + str(item_count)
            order_details_html = ''
            for i in range(1,int(item_count)+1):
                this_item = []
                temp_order_description = ""
                
                str_temp = 'item_name'+ str(i)
                em = re.search('%s=\S+'%str_temp, response_str)
                if em:
                    temp = em.group(0)
                    item_name = temp[11:len(temp)]
                    item_name  = item_name.replace("+"," ")
                    #self.response.out.write(item_name)
                    this_item.append(item_name)
                    temp_order_description = temp_order_description + ' item_name_'+ str(i) + item_name
                    
                str_temp = 'quantity'+ str(i)                
                em = re.search('%s=\d+'%str_temp, response_str)                
                if em:
                    temp = em.group(0)
                    this_item_count = temp[10:len(temp)]                
                    #self.response.out.write(this_item_count)
                    this_item.append(int(this_item_count))
                    temp_order_description = temp_order_description + " item_quantity_" + str(i) + this_item_count
                    
                
                str_temp = 'option_selection2_'+ str(i)                
                em = re.search('%s=\S+'%str_temp, response_str)                
                if em:
                    temp = em.group(0)
                    chef_id = temp[20:len(temp)]                    
                    #self.response.out.write(chef_id)
                    this_item.append(chef_id)
                    temp_order_description = temp_order_description + " item_chef_" + str(i) + chef_id
                
                str_temp = 'option_selection3_'+ str(i)                
                em = re.search('%s=\S+'%str_temp, response_str)                
                if em:
                    temp = em.group(0)
                    delivery_date = temp[20:len(temp)]                    
                    #self.response.out.write(delivery_date)
                    this_item.append(delivery_date)
                    temp_order_description = temp_order_description + " item_delivery_" + str(i) + delivery_date
                
                str_temp = 'mc_gross_'+ str(i)                
                em = re.search('%s=\S+'%str_temp, response_str)                
                if em:
                    temp = em.group(0)
                    total_price = temp[11:len(temp)]                    
                    #self.response.out.write(total_price)
                    this_item.append(total_price)
                    temp_order_description = temp_order_description + " item_price_" + str(i) + total_price
                    
                str_temp = 'option_selection1_'+ str(i)                
                em = re.search('%s=\S+'%str_temp, response_str)                
                if em:
                    temp = em.group(0)
                    item_id = temp[20:len(temp)]                    
                    #self.response.out.write(item_id)
                    this_item.append(item_id)
                    temp_order_description = temp_order_description + " item_id_" + str(i) + item_id
                    
                    #------------Reduce the Quantity of Meal Accordingly-------
                    meal = db.get(item_id)
                    meal.max_quantity = meal.max_quantity-int(this_item_count)
                    meal.put()
                
                item_name_link = "<a href='%s/_meal?m=%s'>" %(home_site,item_id)
                item_name_link = item_name_link + item_name + '</a>'
                order_details_html = order_details_html + '<tr><td style="width:150px;">%s</td>' %item_name_link
                order_details_html = order_details_html + '<td tyle="width:90px;">%s</td>' %total_price
                order_details_html = order_details_html + '<td style="width:120px;">%s</td>' %this_item_count                
                chef_id_link = "<a href='%s/_chef?u=%s'>" %(home_site,chef_id)
                chef_id_link = chef_id_link + chef_id + '</a>'
                order_details_html = order_details_html + '<td style="width:90px;">%s</td></tr>' %chef_id_link
                
                
                order_description = order_description + temp_order_description                  
                delivery_date = str(delivery_date)
                delivery_date = delivery_date.replace('%26nbsp',' ')
                delivery_date = delivery_date.replace('%3A',':')
                
                delivery_date = datetime.strptime(str(delivery_date), "%Y-%m-%d %H:%M:%S")
                
                #self.response.out.write(delivery_address)            
                if userid:
                    b = Orders_DB(order_id = "1",price = payment_amount,chef_id = chef_id,order_status="confirmed",
                         user_id = userid,delivery_address = user_address,delivery_time = delivery_date,order_details = order_description)
                    b.put()
                    d = db.GqlQuery("SELECT * FROM UserPass_User WHERE user_id = '%s' " %userid.lower())
                    l = d.get()
                    id_of_order = str(b.key())
                    ordrs = l.orders
                    ordrs.append(str(b.key()))
                    l.orders = ordrs
                    l.put()
                    
                else:
                    b = Orders_DB(order_id = "1",price = payment_amount,chef_id = chef_id,order_status="confirmed",
                         delivery_address = user_address,delivery_time = delivery_date,order_details = order_description)
                    b.put()
                    id_of_order = str(b.key())
            
        
            
                items_lst.append(this_item)
                
            #------------------------------------------------------------------
            #==================================================================
            
            
            #==============SEND THE CONFIRMATION EMAIL TO THE USER=============
            str0 = '<html> <head><style> td{text-align:center;}</style></head> <body>'
            email_body = '<table cellpadding="0" cellspacing="0" border="0" align="center"> '
            email_body = email_body + '<td width="600" valign="top"><h3><span style="color:#888888">Thank you for your order.</span></h3><h4><span style="color:#888888">Your order has been successfully placed! Your order ID is %s</span></h4></tr></tbody></table>'%id_of_order
            email_body = email_body + '<table cellpadding="5" cellspacing="10" border="0" align="center" style="wdith:100&#37;"> <tbody><tr><td style="width:150px;">Dish name</td> <td tyle="width:60px;">Price</td> <td style="width:60px;">Quantity</td> <td style="width:60px;">Chef</td></tr>'
            email_body = email_body + order_details_html
            email_body = email_body + '</tbody></table><hr> '
            email_body = email_body + '<h4 style="width:80&#37" align="center"><span style="color:#888888;">The order is set to be delivered on <span style="color:#F70D1A;">%s</span> to the following address:</span></h4><br><span style="color:#F70D1A;" align="center">%s</span>' %(delivery_date,user_address)
            email_body = email_body + '<h4 style="width:80&#37" align="center"><span style="color:#888888;">If you need to change any of these details or cancel your order, please <a href="%s/_modify_order?v=%s">click here</a></span></span></h4>' %(home_site,id_of_order)
            str3 = '</body></html>'
            msg_content = str0 + email_body  + str3
            message = mail.EmailMessage(sender="Amir Hesam Salavati <saloot@gmail.com>",
            subject="Order confirmation")
            message.to = "%s" %str(user_email_add)
            message.html = """%s""" %msg_content
                    
   
            message.send()
            #==================================================================
            
            
            #==============SEND THE CONFIRMATION EMAIL TO THE CHEF=============
            str0 = '<html> <head><style> td{text-align:center;}</style></head> <body>'
            email_body = '<table cellpadding="0" cellspacing="0" border="0" align="center"> '
            email_body = email_body + '<td width="600" valign="top"><h3><span style="color:#888888">Congratuldations! You have a new order.</span></h3><h4><span style="color:#888888">The order ID is %s</span></h4></tr></tbody></table>'%id_of_order
            email_body = email_body + '<table cellpadding="5" cellspacing="10" border="0" align="center"> <tbody><tr><td style="width:150px;">Dish name</td> <td tyle="width:60px;">Price</td> <td style="width:60px;">Quantity</td> <td style="width:60px;">Chef</td></tr>'
            email_body = email_body + order_details_html
            email_body = email_body + '</tbody></table><hr> '
            email_body = email_body + '<h4 style="width:80&#37" align="center"><span style="color:#888888;">The order is set to be delivered on <span style="color:#F70D1A;">%s</span> to the following address: <span style="color:#F70D1A;">%s</span></span></h4>' %(delivery_date,user_address)
            email_body = email_body + '<h4 style="width:80&#37" align="center"><span style="color:#888888;">If you have questions regarding your order, please contact us at <a href="%s/contacts">click here</a></span></span></h4>' %(home_site)
            str3 = '</body></html>'
            msg_content = str0 + email_body  + str3
            message = mail.EmailMessage(sender="Amir Hesam Salavati <saloot@gmail.com>",
            subject="Order confirmation")
            message.to = "%s" %str(merchant_email_add)
            message.html = """%s""" %msg_content        
   
            message.send()
            #==================================================================            
            
            
            #===================SCHEDULE A REVIEW EMAIL========================
            taskqueue.add(url='/_reviewemail', params={'order_id': id_of_order,'user_email':user_email_add},countdown=30)
            #==================================================================            
            
            params_new_post['user_address'] = user_address
            params_new_post['id_of_order'] = id_of_order
            params_new_post['delivery_date'] = delivery_date
            params_new_post['order_details_html'] = order_details_html
            
            self.response.out.write(template.render('./html/successful_payment.html',params_new_post))
        else:
            self.response.out.write(template.render('./html/failed_payment.html',''))
        #==============================================================
        
