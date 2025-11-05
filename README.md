# Flask REST API Project

A REST API built with Flask that provides CRUD operations for managing items and web scraping capabilities.

## Features

- Basic CRUD operations for items
- Web scraping endpoints
- Authentication support
- Swagger documentation
- Virtual environment management

## Prerequisites

- Python 3.x
- pip (Python package installer)

## Project Structure

```
aula2-new/
├── app.py              # Main Flask application
├── requirements.txt    # Project dependencies
└── README.md          # Project documentation
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd aula2-new
```

2. Create and activate a virtual environment:

For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

For Linux/Mac:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Ensure your virtual environment is activated
2. Navigate to the aula2-new directory:
```bash
cd aula2-new
```

3. Run the Flask application:
```bash
python app.py
```

4. The server will start on `http://localhost:5000`

## API Authentication

The API uses basic authentication:
- Username: `user`
- Password: `password`

## API Endpoints

### Items Management
- `GET /items`: Retrieve all items
- `POST /items`: Create a new item
- `PUT /items/<item_id>`: Update an item
- `DELETE /items/<item_id>`: Delete an item

### Web Scraping
- `GET /scrape/title`: Scrape webpage title
- `GET /scrape/books`: Scrape book titles from webpage

## API Documentation

Access the Swagger UI documentation at:
```
http://localhost:5000/apidocs/
```

## Example Usage

Using curl with authentication:

```bash
# Get all items
curl -u user:password http://localhost:5000/items

# Create new item
curl -u user:password -X POST -H "Content-Type: application/json" -d "{\"item\":\"orange\"}" http://localhost:5000/items

# Scrape webpage title
curl -u user:password "http://localhost:5000/scrape/title?url=http://example.com"
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.