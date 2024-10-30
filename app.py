from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/products/<item>', methods=['GET'])
def get_products(item):
    limit = request.args.get('limit', default=10, type=int)
    page = request.args.get('page', default=1, type=int)
    
    url = f'https://listado.mercadolibre.com.pe/{item}?Desde={(page-1)*50+1}&NoIndex_True'
    response = requests.get(url + '/' + item)

    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.find_all('div', class_='poly-card')[:limit]
    products_list = []

    for item in products:
        title = item.find('h2', class_='poly-component__title').text
        price = item.find('div', class_='poly-price__current').text
        url = item.find('h2', class_='poly-component__title').find('a').get('href')
        img = item.find('img', class_='poly-component__picture').get('src')
        products_list.append({
            'title': title,
            'price': price,
            'url': url,
            'img': img
        })

    return jsonify(products_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)