from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/products/<item>', methods=['GET'])
def get_products(item):
    limit = request.args.get('limit', default=50, type=int)
    page = request.args.get('page', default=1, type=int)

    url = f'https://listado.mercadolibre.com.pe/{item}_Desde_{(page-1)*50+1}_NoIndex_True'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
   
    products = soup.find_all('div', class_='poly-card')[:limit]
    products_list = []

    for product in products:
        title = product.find('h2', class_='poly-component__title').text if product.find('h2', class_='poly-component__title') else "Sin título"
        price = product.find('div', class_='poly-price__current').text if product.find('div', class_='poly-price__current') else "Sin precio"
        url = product.find('h2', class_='poly-component__title').find('a').get('href') if product.find('h2', class_='poly-component__title') and product.find('h2', class_='poly-component__title').find('a') else "Sin URL"
        img = product.find('img', class_='poly-component__picture').get('src') if product.find('img', class_='poly-component__picture') else "Sin imagen"
        
        products_list.append({
            'title': title,
            'price': price,
            'url': url,
            'img': img
        })
    
    return jsonify(products_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
