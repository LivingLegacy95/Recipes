from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_app import flash


DATABASE = "recipes"


class Recipe:

    def __init__(self, data) -> None:
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.cook_time = data['cook_time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = data['creator']
        self.user_id = data['user_id']

    def show_first_name(self):
        return self.first_name

    #! Create
    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes(name, description, instructions, cook_time, user_id) VALUES(%(name)s, %(description)s, %(instructions)s, %(cook_time)s, %(user_id)s) ;"
        return connectToMySQL(DATABASE).query_db(query, data)

    #! READ ALL

    @classmethod
    def get_all(cls):
        query = "Select * FROM recipes JOIN users ON recipes.user_id = users.id;"
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        recipes = []
        for recipe in results:
            creator = User.find_by_id(recipe['user_id'])
            recipe['creator'] = creator
            recipes.append(Recipe(recipe))
        return recipes

    #!READ ONE
    @classmethod
    def get_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        print(result[0])
        for recipe in result:
            creator = User.find_by_id(recipe['user_id'])
            recipe['creator'] = creator
            recipe = Recipe(result[0])
        return recipe

    #! UPDATE
    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    #! Delete
    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @staticmethod
    def validate_recipe(recipe:dict):
        is_valid = True
        if len(recipe['name']) < 3:
            flash("*recipe name must contain at least 3 character*")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("*recipe description must contain at least 3 character*")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("*recipe instructions must contain at least 3 character*")
            is_valid = False
        # if recipe['created_at'] == "":
        #     flash("Cook date is required")
        #     is_valid = False
        return is_valid
    
