#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response,jsonify
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
        pizzas = [pizza.to_dict() for pizza in Pizza.query.all()]
        response = make_response(pizzas, 200)
        return response
api.add_resource(Pizzas, '/pizzas')

class PizzaByID(Resource):
    def get(self, id):
        pizza = Pizza.query.filter_by(id=id).first()
        pizza_dict = pizza.to_dict()
        response = make_response(pizza_dict, 200)
        return response
api.add_resource(PizzaByID, '/pizzas/<int:id>')

class Restaurants(Resource):
    def get(self):
        restaurants = [restaurant.to_dict() for restaurant in Restaurant.query.all()]

        response = make_response(restaurants, 200)

        return response
api.add_resource(Restaurants, '/restaurants')

class RestaurantByID(Resource):
    def get(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()

        if restaurant:
            restaurant_dict = restaurant.to_dict()
            response = make_response(restaurant_dict,200)
            return response
        else:
            response_body = {
                "error": "Restaurant not found"
            }
            return make_response(response_body, 404)

    def delete(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()

            response_body = {
             
            }
            return make_response(response_body, 204)
        
        else:
            response_body = {
                "error": "Restaurant not found"
            }
            return make_response(response_body, 404)

api.add_resource(RestaurantByID, '/restaurants/<int:id>')

class RestaurantPizzas(Resource):
    def get(self):
        restaurantpizzas = [restaurantpizza.to_dict() for restaurantpizza in RestaurantPizza.query.all()]

        response = make_response(restaurantpizzas,200)

        return response
    
    def post(self):
        new_restaurant_pizza = RestaurantPizza(
              price = request.json['price'],
              pizza_id = request.json['pizza_id'],
              restaurant_id = request.json['restaurant_id']
        )
        db.session.add(new_restaurant_pizza)
        db.session.commit()

        restaurant_pizza_to_dict = new_restaurant_pizza.to_dict()

        response = make_response(restaurant_pizza_to_dict, 201)

        return response
        
api.add_resource(RestaurantPizzas, '/restaurant_pizzas')

class RestaurantPizzaByID(Resource):
    def get(self, id):
        restaurantpizza = RestaurantPizza.query.filter_by(id=id).first().to_dict()

        return make_response(restaurantpizza, 200)

api.add_resource(RestaurantPizzaByID, '/restaurant_pizzas/<int:id>')


if __name__ == "__main__":
    app.run(port=5555, debug=True)
