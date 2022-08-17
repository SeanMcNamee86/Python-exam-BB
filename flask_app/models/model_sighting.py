from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import model_user
from flask import flash




class Sighting:
    def __init__( self , data ):
        self.id = data['id']
        self.location = data['location']
        self.description = data['description']
        self.num_sighted = data['num_sighted']
        self.created_at = data['created_at']
        self.date_sighted = data["date_sighted"]
        self.updated_at = data['updated_at']
        self.users_id = data["users_id"]

    @classmethod
    def create_one(cls, data):
        query = "INSERT INTO sightings (location, description, num_sighted, users_id, date_sighted) values( %(location)s, %(description)s, %(num_sighted)s, %(users_id)s, %(date_sighted)s)"
        return connectToMySQL(DATABASE).query_db(query, data)
        

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM sightings;"
        results = connectToMySQL(DATABASE).query_db(query)
        sighting = []
        for user in results:
            sighting.append( cls(user) )
        return sighting

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM sightings JOIN users ON sightings.users_id = users.id WHERE sightings.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        for result in results:
            user_data = {
                **result,
                "id" : result["users.id"],
                "created_at" : result["users.created_at"],
                "updated_at" : result["users.updated_at"]
            }
            sighting = cls(result)
        sighting.user = model_user.User(user_data)
        Sighting.get_skeptics_and_attach(sighting, {"id" : sighting.id})
        return sighting

    @classmethod
    def update_one(cls, data):
        query = "UPDATE sightings SET location = %(location)s, description = %(description)s, num_sighted = %(num_sighted)s, date_sighted = %(date_sighted)s where id = %(id)s"
        connectToMySQL(DATABASE).query_db(query, data)
        return cls

    @classmethod
    def delete_one(cls, data):
        query = "DELETE from sightings where id = %(id)s"
        connectToMySQL(DATABASE).query_db(query, data)
        return cls

    @classmethod
    def get_all_sightings_with_users(cls):
        query = "SELECT * FROM sightings JOIN users ON sightings.users_id = users.id"
        results = connectToMySQL(DATABASE).query_db(query)
        all_sightings = []
        for result in results:
            user_data = {
                **result,
                "id" : result["users.id"],
                "created_at" : result['users.created_at'],
                "updated_at" : result['users.updated_at']
            }
            result = cls(result)
            result.user = model_user.User(user_data)
            all_sightings.append(result)
            data = {
                "id" :result.id
            }
            Sighting.get_skeptics_and_attach(result, data)
        return all_sightings

    @classmethod
    def get_skeptics_and_attach(cls, sighting, data):
        query = "SELECT * FROM sightings left join sightings_has_skeptics on sightings.id = sightings_has_skeptics.sightings_id join users on sightings_has_skeptics.users_id = users.id where sightings.id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        sighting.skeptics = []
        for result in results:
                user_data = {
                **result,
                "id" : result["users.id"],
                "created_at" : result["users.created_at"],
                "updated_at" : result["users.updated_at"]
                }
                sighting.skeptics.append(model_user.User(user_data))
        print(sighting.skeptics)
        return sighting


    @staticmethod
    def validate_sighting(sighting):
        is_valid = True
        if len(sighting["location"]) < 3:
            is_valid = False
            flash("location must be longer than 3 characters")
        if len(sighting["num_sighted"]) < 1:
            is_valid = False
            flash("There must be at least 1 sasquatch to report sighting")
        if len(sighting["description"]) < 3:
            is_valid = False
            flash("description must be longer than 3 characters")
        if len(sighting["date_sighted"]) < 1:
            is_valid = False
            flash("you must select a valid date")

        return is_valid

    @classmethod
    def user_is_skeptic(cls, data):
        query = "select * from sightings_has_skeptics where users_id = %(user_id)s and sightings_id = %(sighting_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results:
            return False
        else:
            return True
