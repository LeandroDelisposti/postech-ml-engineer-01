import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, 
    create_access_token,
    jwt_required, 
    get_jwt_identity
)
import bcrypt

app = Flask(__name__)
app.config.from_object('config')
  
auth = HTTPBasicAuth()

db = SQLAlchemy(app)
jwt = JWTManager(app)
swagger = Swagger(app)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    time_minutes = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'ingredients': self.ingredients,
            'time_minutes': self.time_minutes 
        }
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route('/register', methods=['POST'])
def register_user():
    """Register a new user.
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
            type: object
            properties:
                username:
                    type: string
                password:
                    type: string
    responses:
        201:
            description: User registered successfully
        400:
            description: User already exists
    """
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify(message="User already exists"), 400
    
    salt = bcrypt.gensalt(rounds=12)
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), salt)
    new_user = User(username=data['username'], password=hashed_password)
    
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="User registered"), 201

@app.route('/login', methods=['POST'])
def login():
    """User login to get JWT token.
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
            type: object
            properties:
                username:
                    type: string
                password:
                    type: string
    responses:
        200:
            description: Login successful
        401:
            description: Invalid credentials
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()

    if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify(error="Invalid credentials"), 401

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/recipes', methods=['POST'])
@jwt_required()
def create_recipe():
    """Create a new recipe.
    ---
    security:
        - BearerAuth: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
            type: object
            required: true
            properties:
                name:
                    type: string
                description:
                    type: string
                ingredients:
                    type: string
                time_minutes:
                    type: integer
    responses:
        201:
            description: Recipe created successfully
        401:
            description: Unauthorized"""
    data = request.get_json()
    new_recipe = Recipe(
        name=data['name'],
        description=data['description'],
        ingredients=data['ingredients'],
        time_minutes=data['time_minutes']
    )
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify(new_recipe.to_dict()), 201

@app.route('/recipes', methods=['GET'])
@jwt_required()
def get_recipes():
    """Get all recipes.
    ---
    security:
        - BearerAuth: []
    parameters:
      - in: query
        name: page
        type: integer
        required: false
        description: Filter by ingredient
      - in: query
        name: max_time
        type: integer
        required: false
        description: Max preparation time in minutes
    responses:
        200:
            description: A list of recipes
            schema:
                type: array
                items:
                    type: object
                    properties:
                        id:
                            type: integer
                        name:
                            type: string
                        description:
                            type: string
                        ingredients:
                            type: string
                        time_minutes:
                            type: integer
    """
    ingredient = request.args.get('ingredient')
    max_time = request.args.get('max_time', type=int)
    query = Recipe.query    
    if ingredient:
        query = query.filter(Recipe.ingredients.ilike(f'%{ingredient}%'))
    if max_time is not None:
        query = query.filter(Recipe.time_minutes <= max_time)
    
    recipes = query.all()
    return jsonify([recipe.to_dict() for recipe in recipes]), 200


@app.route('/recipes/<int:recipe_id>', methods=['PUT'])
@jwt_required()
def update_recipe(recipe_id):
    """Update a recipe by ID.
    ---
    security:
        - BearerAuth: []
    parameters:
      - in: path
        name: recipe_id
        type: integer
        required: true
        description: ID of the recipe to update
      - in: body
        name: body
        required: true
        schema:
            type: object
            properties:
                name:
                    type: string
                description:
                    type: string
                ingredients:
                    type: string
                time_minutes:
                    type: integer
    responses:
        200:
            description: Recipe updated successfully
        404:
            description: Recipe not found
        401:
            description: Unauthorized
    """
    data = request.get_json()
    recipe = Recipe.query.get_or_404(recipe_id)
    if 'name' in data:
        recipe.name = data['name']
    if 'description' in data:
        recipe.description = data['description']
    if 'ingredients' in data:
        recipe.ingredients = data['ingredients']
    if 'time_minutes' in data: 
        recipe.time_minutes = data['time_minutes']
    db.session.commit()
    return jsonify(recipe.to_dict()), 200

@app.route('/recipes/<int:recipe_id>', methods=['DELETE'])
@jwt_required()
def delete_recipe(recipe_id):
    """Delete a recipe by ID.
    ---
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: recipe_id
        type: integer
        required: true
        description: ID of the recipe to delete
    responses:
        200:
            description: Recipe deleted successfully
        404:
            description: Recipe not found
        401:
            description: Unauthorized
    """
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({"message": "Recipe deleted successfully"}), 200

@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    