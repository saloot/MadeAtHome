from google.appengine.ext import db

class Orders_DB(db.Model):
    order_id = db.StringProperty(required = True)
    price = db.FloatProperty(required = True)
    chef_id = db.StringProperty(required = True)
    user_id = db.StringProperty(required = False)
    delivery_address = db.TextProperty(required = True)
    delivery_time = db.DateTimeProperty(required = True)
    rating = db.IntegerProperty(required = False)
    comments = db.TextProperty(required = False)
    created_date = db.DateTimeProperty(auto_now_add = False)
    reviewed = db.IntegerProperty(required = False, default = 0)
    order_details = db.TextProperty(required = True)
    order_status = db.StringProperty(required = True)

class Reviews_DB(db.Model):
    chef_id = db.StringProperty(required = True)
    user_id = db.StringProperty(required = False)
    comments = db.TextProperty(required = False)
    order_id = db.StringProperty(required = False)
    rating = db.IntegerProperty(required = False)
    title = db.StringProperty(required = True)
    
class Messages_DB(db.Model):
    sender_id = db.StringProperty(required = True)
    recepient_id = db.StringProperty(required = True)
    message_body = db.TextProperty(required = True)
    created_date = db.DateTimeProperty(auto_now_add = True)
    message_title = db.StringProperty(required = True)
    message_parent = db.StringProperty(required = False)
    read_status = db.IntegerProperty(required = True, default = 0)    
    new_conversation = db.IntegerProperty(required = True, default = 1)

class UserPass_Chef(db.Model):
    user_id = db.StringProperty(required = True)    
    user_firstname = db.StringProperty(required = True)
    user_lastname = db.StringProperty(required = True)
    user_address = db.TextProperty(required = True)
    created_date = db.DateTimeProperty(auto_now_add = True)
    user_email = db.StringProperty(required = True)
    user_latitude = db.StringProperty(required = True)
    user_longitude = db.StringProperty(required = True)
    user_phone = db.StringProperty(required = True)
    user_bankacnt = db.StringProperty(required = True)
    user_rating = db.IntegerProperty(required = False, default = 0)
    no_reviews = db.IntegerProperty(required = False, default = 0)    
    restaurant_name = db.StringProperty(required = True)
    
class UserPass_User(db.Model):
    user_id = db.StringProperty(required = True)
    user_pass = db.StringProperty(required = True)
    user_firstname = db.StringProperty(required = False)
    user_lastname = db.StringProperty(required = False)
    user_address = db.TextProperty(required = False)
    user_phone = db.StringProperty(required = False)
    created_date = db.DateTimeProperty(auto_now_add = True)
    user_email = db.StringProperty(required = False)
    user_latitude = db.StringProperty(required = False)
    user_longitude = db.StringProperty(required = False)
    user_bonus = db.IntegerProperty(required = False, default = 0)
    ischef = db.IntegerProperty(required = False, default = 0)
    orders = db.ListProperty(str)
    
class FoodList(db.Model):
    chef_id = db.StringProperty(required = True)
    meal_type = db.StringProperty(required = True)
    title = db.StringProperty(required = True)
    ingredients = db.StringListProperty(required = True)
    max_quantity = db.IntegerProperty(required = True)
    price = db.IntegerProperty(required = True)
    description = db.TextProperty(required = True)
    chef_firstname = db.StringProperty(required = True)
    chef_lastname = db.StringProperty(required = True)
    chef_address = db.TextProperty(required = True)
    created_date = db.DateTimeProperty(auto_now_add = True)
    offered_date_begin = db.DateTimeProperty(required = True)
    offered_date_finish = db.DateTimeProperty(required = True)
    chef_email = db.StringProperty(required = True)
    chef_latitude = db.StringProperty(required = True)
    chef_longitude = db.StringProperty(required = True)
    chef_phone = db.StringProperty(required = True)
    chef_bankacnt = db.StringProperty(required = True)
    food_image1 = db.BlobProperty(required = True)
    food_image2 = db.BlobProperty(required = False)
    food_image3 = db.BlobProperty(required = False)
    food_image4 = db.BlobProperty(required = False)
    food_image5 = db.BlobProperty(required = False)
    meal_promotion_msg = db.StringProperty(required = False)
    
class FoodTitles(db.Model):    
    title = db.StringProperty(required = True)
    food_type = db.StringProperty(required = False)

class IngredientsTitles(db.Model):    
    title = db.StringProperty(required = True)
    ingredient_type = db.StringProperty(required = False)

