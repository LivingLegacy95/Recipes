from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

DATABASE = "recipes"

class User:

    def __init__(self, data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def find_by_email(cls, email):
        query = "SELECT * FROM users WHERE email = %(email)s";
        data = {'email': email}
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) > 0:
            return User(result[0])
        else:
            return False

    @classmethod
    def find_by_id(cls, id):
        query = "SELECT * FROM users WHERE id = %(id)s";
        data = {'id': id}
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) > 0:
            return User(result[0])
        else:
            return False


    @staticmethod
    def validate_user(user: dict):
        is_valid = True 
        if len(user['first_name']) < 2:
            is_valid = False
            flash("*First Name must contain at least 2 characters*")
        if len(user['last_name']) < 4:
            is_valid = False
            flash("*Last Name must contain at least 4 characters*")
        if user['password'] != user['confirm_password']:
            is_valid = False 
            flash("*Password must match*")
        if not EMAIL_REGEX.match(user['email']): 
            flash("*Invalid email address*")
            is_valid = False

        return is_valid
