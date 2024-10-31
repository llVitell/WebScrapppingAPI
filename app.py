from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def extract_image(img_elem):
    image_attributes = ['data-src', 'src']
    
    for attr in image_attributes:
        if img_elem and img_elem.has_attr(attr):
            img = img_elem[attr]
            if img and not img.startswith('data:image'):
                return img
    
    return None

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
        title = product.find('h2', class_='poly-component__title').text
        price = product.find('div', class_='poly-price__current').text
        url = product.find('h2', class_='poly-component__title').find('a').get('href')
        img_elem = product.find('img', class_='poly-component__picture')
        img = extract_image(img_elem)

        products_list.append({
            'title': title,
            'price': price,
            'url': url,
            'img': img
        })
    
    return jsonify(products_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
