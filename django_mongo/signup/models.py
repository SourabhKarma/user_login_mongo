from django.db import models
from django_mongo.settings import db
# Create your models here.


signup_collection = db['project1_system']




import pymongo

# class CustomUser:
#     # collection = db['users']
#     signup_collection = db['project1_system']

#     @classmethod
#     def create(cls, phone_number, password):
#         user_data = {
#             'phone_number': phone_number,
#             'password': password,
#             # Add other user profile fields as needed
#         }
#         return cls.collection.insert_one(user_data)

#     @classmethod
#     def get_by_phone_number(cls, phone_number):
#         return cls.signup_collection.find_one({'phone_number': phone_number})


class CustomUser:
    signup_collection = db['project1_system']  # Use the correct collection name

    @classmethod
    def create_user(cls, phone_number, password):
        user_data = {
            'phone_number': phone_number,
            'password': password,
            # Add other user profile fields as needed
        }
        cls.signup_collection.insert_one(user_data)