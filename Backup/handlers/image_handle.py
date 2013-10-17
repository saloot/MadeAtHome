import webapp2
from google.appengine.api import memcache
from google.appengine.ext import db
import time
from dbs.databases import *

class ImageHandler (webapp2.RequestHandler):
  def get(self):
    meal_key=self.request.get('k')
    meal_img_no=int(self.request.get('n'))
    meal = db.get(meal_key)
    
    if (meal_img_no == 1):
      if meal.food_image1:
        self.response.headers['Content-Type'] = "image/png"
        self.response.out.write(meal.food_image1)
      else:
       self.error(404)
    elif (meal_img_no == 2):
      if meal.food_image2:
        self.response.headers['Content-Type'] = "image/png"
        self.response.out.write(meal.food_image2)
      else:
       self.error(404)
    elif (meal_img_no == 3):
      if meal.food_image3:
        self.response.headers['Content-Type'] = "image/png"
        self.response.out.write(meal.food_image3)
      else:
       self.error(404)
    elif (meal_img_no == 4):
      if meal.food_image4:
        self.response.headers['Content-Type'] = "image/png"
        self.response.out.write(meal.food_image4)
      else:
       self.error(404)
    elif (meal_img_no == 5):
      if meal.food_image5:
        self.response.headers['Content-Type'] = "image/png"
        self.response.out.write(meal.food_image5)
      else:
       self.error(404)
    else:
      self.error(404)