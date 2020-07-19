"""
MY FIRST FLASK APP
"""

from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [
    {
        'name': 'aldi',
        'items': [
            {
                'name': 'My Item',
                'price': 15.99
            }
        ]
    }
]


@app.route('/')
def home():
    """

    :return:
    """
    return render_template('index.html')


# POST --> used to receive data
# GET --> used to send data back only

# POST /store_data: {name: }
@app.route('/store', methods=['POST'])
def create_store():
    """
    Create store Endpoint.
    """
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)


# GET /store/<string:name>
@app.route('/store/<string:name>')  # 'http://127.0.0.1:5000/store/aldi'
def get_store(name):
    """
    Get one store.
    :param name:
    """
    for store in stores:
        if store.get("name") == name:
            return jsonify(store)
    return jsonify({'message': "The name is not available"})


# GET /store
@app.route('/store')
def get_stores():
    """
    Get stores.
    """
    return jsonify({"stores": stores})


# POST /store/<string:name>/item {name: ,price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    """
    Create items in store.
    """
    request_data = request.get_json()
    for store in stores:
        if store.get('name') == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return ({'message': 'store not found'})


# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    """
    Get items in store.
    """
    for store in stores:
        if store.get('name') == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': "Store not found"})


app.run(port=5000)
