import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from flasgger import Swagger

app = Flask(__name__)

app.config['SWAGGER'] = {
    'title': 'Library Flask API',
    'uiversion': 3
}

swagger = Swagger(app)

auth = HTTPBasicAuth()

users = {
    "user": "password"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

@app.route('/')
def home():
    return "Hello, Flask!"

items = ['apple', 'banana', 'cherry']

@app.route('/items', methods=['GET'])
@auth.login_required
def get_items():
    return jsonify({'items': items})

@app.route('/items', methods=['POST'])
@auth.login_required
def create_item():
    new_item = request.json.get('item')
    if new_item:
        items.append(new_item)
        return jsonify({'item': new_item, 'success': 'Item added successfully!'}), 201
    return jsonify({'warning': 'Invalid item!'}), 400

@app.route('/items/<int:item_id>', methods=['PUT'])
@auth.login_required
def update_item(item_id):
    updated_item = request.json.get('item')
    if updated_item and 0 <= item_id < len(items):
        items[item_id] = updated_item
        return jsonify({'item': updated_item, 'success': 'Item updated successfully!'}), 200
    return jsonify({'warning': 'Invalid item!'}), 404

@app.route('/items/<int:item_id>', methods=['DELETE'])
@auth.login_required
def delete_item(item_id):
    if 0 <= item_id < len(items):
        removed_item = items.pop(item_id)
        return jsonify({'item': removed_item, 'success': 'Item deleted successfully!'}), 200
    return jsonify({'warning': 'Invalid item!'}), 404

@app.route('/scrape/title', methods=['GET'])
@auth.login_required
def scrape_title():
    """Endpoint to scrape the title of a given webpage.
    ---
    parameters:
      - name: url
        in: query
        type: string
        required: true
    responses:
      200:
        description: Title scraped successfully
        schema:
          type: object
          properties:
            title:
              type: string
            success:
              type: string
              example: "Success!"
      404:
        description: Title not found
        schema:
          type: object
          properties:
            warning:
              type: string
              example: "No title found"
    """

    url = request.args.get('url')

    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        print('Pagina obtida com sucesso!')
    else:
        print(f'Erro {response.status_code} ao acessar a página.')
        return jsonify({'error': 'Error occurred while scraping'}), 500

    return jsonify({'title': soup.title.string, 'success': 'Success!'}) if soup.title else jsonify({'warning': 'No title found'}), 404

@app.route('/scrape/books', methods=['GET'])
@auth.login_required
def scrape_books():
    """Endpoint to scrape book titles from a given webpage.
    ---
    parameters:
      - name: url
        in: query
        type: string
        required: true
    responses:
      200:
        description: Books scraped successfully
        schema:
          type: object
          properties:
            books:
              type: array
              items:
                type: string
            success:
              type: string
              example: "Success!"
      404:
        description: No books found
        schema:
          type: object
          properties:
            warning:
              type: string
              example: "No books found"
    """

    url = request.args.get('url')

    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        print('Pagina obtida com sucesso!')
    else:
        print(f'Erro {response.status_code} ao acessar a página.')
        return jsonify({'error': 'Error occurred while scraping'}), 500

    books = [book.string for book in soup.find_all('h3')]
    if books:
        return jsonify({
            'books': books, 
            'success': 'Books scraped successfully!'
        }), 200
    return jsonify({'warning': 'No books found'}), 404

if __name__ == '__main__':
    app.run(debug=True)