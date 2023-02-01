from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import users_models
from flask_app.models import purchases_models
from flask import flash


db = 'black_belt'

class Car:
    def __init__(self, data):
        self.id = data['id']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.description = data['description']
        self.price = data['price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.purchased_car = None
        self.seller = None

    @staticmethod
    def valdiate_car(car):
        is_valid = True
        if len(car['model']) < 1:
            flash("Model must not be left blank.")
            is_valid = False
        if len(car['make']) < 1:
            flash("Make must not be left blank.")
            is_valid = False
        if len(car['year']) < 4:
            flash("Please enter a valid year.")
            is_valid = False
        if len(car['description']) < 2:
            flash("Please enter a description")
            is_valid = False
        if len(car['price']) < 1:
            flash("Please enter a valid price.")
            is_valid = False
        return is_valid

    @classmethod
    def get_all_cars(cls):
        query = "SELECT * from car LEFT JOIN purchase ON car.id = purchase.car_id JOIN user on car.user_id = user.id;"
        results = connectToMySQL(db).query_db(query)
        all_cars = []
        for row in results:
            one_car = cls(row)
            one_car.purchased_car = purchases_models.Purchase(
                {
                    'user_id': row['user_id'],
                    'car_id':row['car_id']
                }
            )
            one_car.seller = users_models.User(
                {
                'id': row['user.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
                }
            )
            all_cars.append(one_car)
        return all_cars

    @classmethod
    def add_car(cls, data):
        query = "INSERT INTO car (model, make, year, description, price, user_id) VALUES (%(model)s, %(make)s, %(year)s, %(description)s, %(price)s, %(user_id)s);"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM car WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)


    @classmethod
    def get_one_car(cls, data):
        query = "SELECT * FROM car JOIN user ON user.id = car.user_id WHERE car.id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        car = cls(results[0])
        car.seller = results[0]['first_name']
        return car

    @classmethod
    def update(cls,data):
        query = "UPDATE car SET model = %(model)s, make = %(make)s, year = %(year)s, description = %(description)s, price = %(price)s WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)