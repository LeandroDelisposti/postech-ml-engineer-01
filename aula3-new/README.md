# Flask REST API Demo

A simple REST API built with Flask demonstrating basic CRUD operations for managing items.

## Features

- List all items
- Create new items
- Update existing items
- Delete items

## Prerequisites

- Python 3.x
- pip (Python package manager)

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd aula3-new
   ```

2. **Create and activate a virtual environment:**

   On Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   On Linux/Mac:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Make sure your virtual environment is activated.
2. Run the Flask application:
   ```bash
   python app.py
   ```
3. The server will start on `http://localhost:5000`.

## API Endpoints

- `POST /register`: Register a new user.
  - Body: `{"username": "user", "password": "password"}`
- `POST /login`: User login to get JWT token.
  - Body: `{"username": "user", "password": "password"}`
- `GET /protected`: A protected route, just for testing the token.
- `POST /recipes`: Create a new recipe.
  - Body: `{"name": "recipe_name", "description": "recipe_description", "ingredients": "recipe_ingredients", "time_minutes": "recipe_time_minutes"}`
- `GET /recipes`: Get all recipes.
- `PUT /recipes/<recipe_id>`: Update a recipe by ID.
  - Body: `{"name": "new_recipe_name", "description": "new_recipe_description", "ingredients": "new_recipe_ingredients", "time_minutes": "new_recipe_time_minutes"}`
- `DELETE /recipes/<recipe_id>`: Delete a recipe by ID.

## Example Usage

Using curl or Postman:

```bash
# Register a new user
curl -X POST -H "Content-Type: application/json" -d "{\"username\":\"user\",\"password\":\"password\"}" http://localhost:5000/register

# Login to get a token
curl -X POST -H "Content-Type: application/json" -d "{\"username\":\"user\",\"password\":\"password\"}" http://localhost:5000/login

# Create a new recipe
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d "{\"name\":\"orange juice\",\"description\":\"a simple recipe for orange juice\",\"ingredients\":\"orange, water, sugar\",\"time_minutes\":5}" http://localhost:5000/recipes

# Get all recipes
curl -H "Authorization: Bearer <token>" http://localhost:5000/recipes

# Update a recipe
curl -X PUT -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d "{\"name\":\"mango juice\",\"description\":\"a simple recipe for mango juice\",\"ingredients\":\"mango, water, sugar\",\"time_minutes\":5}" http://localhost:5000/recipes/1

# Delete a recipe
curl -X DELETE -H "Authorization: Bearer <token>" http://localhost:5000/recipes/1
```

## Development

The application runs in debug mode by default, which provides detailed error messages and auto-reloads when code changes are detected.

## License

This project is licensed under the MIT License.