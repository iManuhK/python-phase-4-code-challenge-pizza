#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        response_dict = {
            "message": "Code Challenge Accepted!",
        }

        response = make_response(
            response_dict,
            200,
        )
        return response

api.add_resource(Home, '/')

class Pizzas(Resource):
    def get(self):
        pass
api.add_resource(Pizzas, '/pizzas')

class PizzaByID(Resource):
    def get(self, id):
        pass
api.add_resource(PizzaByID, '/pizzas/<int:id>')

class Restaurants(Resource):
    def get(self):
        pass
api.add_resource(Restaurants, '/restaurants')

class RestaurantByID(Resource):
    def get(self, id):
        pass
api.add_resource(RestaurantByID, '/restaurants/<int:id>')

class RestaurantPizzas(Resource):
    def get(self):
        pass
api.add_resource(RestaurantPizzas, '/restaurant_pizzas')

class RestaurantPizzaByID(Resource):
    def get(self, id):
        pass
api.add_resource(RestaurantPizzaByID, '/restaurant_pizzas/<int:id>')


if __name__ == "__main__":
    app.run(port=5555, debug=True)
