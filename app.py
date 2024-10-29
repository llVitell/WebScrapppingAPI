from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/products/<item>', methods=['GET'])
def get_products(item):
    url = 'https://listado.mercadolibre.com.pe'
    response = requests.get(url + '/' + item)
    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.find_all('div', class_='poly-card')
    products_list = []
    for item in products:
        title = item.find('h2', class_='poly-component__title').text
        price = item.find('div', class_='poly-price__current').text
        products_list.append({
            'title': title,
            'price': price
        })
    return jsonify(products_list)

if __name__ == '__main__':
    app.run(debug=True)    