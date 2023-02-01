from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import cars_models
from flask_app.models import purchases_models
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

db = 'black_belt'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.purchased_car = None

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) == 0 or len(user['last_name']) == 0 or len(user['email']) == 0 or len(user['password']) == 0 or len(user['confirm_password']) == 0:
            flash("All fields required")
            is_valid = False
        if len(user['first_name']) < 2:
            flash("First name must be at least 3 characters.")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address.")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.",)
            is_valid = False
        if not re.search("[A-Z]", user['password']):
            flash("Password must contain at least one capital letter.")
        if not re.search("[0-9]", user['password']):
            flash("Password must contain at least one number.")
        if user['password'] != user['confirm_password']:
            flash("Passwords must match", 'confirm_password')
        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO user (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s )"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM user WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])


    @classmethod
    def show_all_purchases(cls, data):
        query = "SELECT * FROM user JOIN purchase ON user.id = purchase.user_id JOIN car ON purchase.car_id = car.id WHERE user.id = %(id)s;"
        results = connectToMySQL(db).query_db(query,data)
        all_purchases = []
        for row in results:
            print(row)
            one_purchase = cls(row)
            one_purchase.purchased_car = cars_models.Car(
                {
                'id': row['car.id'],
                'model': row['model'],
                'make': row['make'],
                'year': row['year'],
                'description': row['description'],
                'price': row['price'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'user_id' : row['user_id']
                }
            )
            all_purchases.append(one_purchase)
        return all_purchases