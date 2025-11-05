# Flask REST API Demo

A simple REST API built with Flask demonstrating basic CRUD operations for managing items.

## Features

- List all items
- Create new items
- Update existing items
- Delete items

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd aula2-new
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install required dependencies:
Go to aula2-new folder and run:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Make sure your virtual environment is activated
2. Run the Flask application:
```bash
python app.py
```
3. The server will start on `http://localhost:5000`

## API Endpoints

- `GET /items`: Get list of all items
- `POST /items`: Create a new item
  - Body: `{"item": "item_name"}`
- `PUT /items/<item_id>`: Update an item by ID
  - Body: `{"item": "new_item_name"}`
- `DELETE /items/<item_id>`: Delete an item by ID

## Example Usage

Using curl or Postman:

```bash
# Get all items
curl http://localhost:5000/items

# Create new item
curl -X POST -H "Content-Type: application/json" -d "{\"item\":\"orange\"}" http://localhost:5000/items

# Update item at index 0
curl -X PUT -H "Content-Type: application/json" -d "{\"item\":\"mango\"}" http://localhost:5000/items/0

# Delete item at index 0
curl -X DELETE http://localhost:5000/items/0
```

## Development

The application runs in debug mode by default, which provides detailed error messages and auto-reloads when code changes are detected.