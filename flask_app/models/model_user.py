# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
from flask import flash
import re
from flask_bcrypt import Bcrypt
from flask_app import DATABASE, app


bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data["password"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.full_name = f"{self.first_name} {self.last_name}"
        self.skeptic_count = 0
    
    # Now we use class methods to query our database

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE ID = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DATABASE).query_db(query, data)
        for user in results:
            user = cls(user) 
        return user

    @classmethod
    def check_matching_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if not result:
            return  False
        else:
            return True

    @classmethod
    def create_one(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) values( %(first_name)s, %(last_name)s, %(email)s, %(pw)s);"
        connectToMySQL(DATABASE).query_db(query, data)
        return cls

    @staticmethod
    def validate_user( user ):
        is_valid = True

        if len(user["first_name"]) < 2:
            is_valid = False
            flash("invalid first name, must be at least 2 characters in length")
        if len(user["last_name"]) < 2:
            is_valid = False
            flash("Invalid last name, must be at least 2 characters in length")
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(user["pw"]) < 8 or user["pw"] != user["confirm_pw"]:
            flash("Invalid password or password fields do not match")
            is_valid = False
        if User.check_matching_email(user):
            flash("email already in use")
            is_valid = False
        if is_valid:
            flash("Registration success!")
        return is_valid
    
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if not result:
            return False
        return cls(result[0])

    @staticmethod
    def validate_login(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(user["pw"]) < 8:
            flash("password must be at least 8 characters in length")
            is_valid = False
        return is_valid
    @classmethod
    def make_skeptic(cls, data):
        query = "insert into sightings_has_skeptics (users_id, sightings_id) values (%(user_id)s, %(sighting_id)s)"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete_skeptic(cls, data):
        query = "Delete from sightings_has_skeptics where users_id = %(user_id)s and sightings_id = %(sighting_id)s"
        return connectToMySQL(DATABASE).query_db(query, data)