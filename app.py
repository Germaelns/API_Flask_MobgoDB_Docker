from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'api_db'
app.config['MONGO_URI'] = 'mongodb://db:27017/api_db'

mongo = PyMongo(app)


# use URL order?service=service&operator=operator
@app.route('/order', methods=['GET'])
def view_order():
    order = mongo.db.order
    service = request.args['service']
    operator = request.args['operator']
    q = order.find_one({'service': service, 'operator': operator})
    if q:
        result = {'service': q['service'], 'operator': q['operator'], 'price': price}
    else:
        result = 'No results found'

    return jsonify({'result': result})


# use URL order?service=service&operator=Nikolay&price=200
@app.route('/order', methods=['POST'])
def add_order():
    service = request.args['service']
    operator = request.args['operator']
    price = request.args['price']

    order = mongo.db.order
    order.insert({'service': service, 'operator': operator, 'price': price})

    return 'Order added!'


# use URL order?service=service&operator=Nikolay&price=200
@app.route('/order', methods=['DELETE'])
def delete_order():
    order = mongo.db.order
    service = request.args['service']
    operator = request.args['operator']
    price = request.args['price']
    query = order.delete_one({'service': service, 'operator': operator, 'price': price})

    if query:
        return 'Order deleted!!'
    else:
        return 'Order not found!!'


@app.route('/order/all', methods=['GET'])
def all_orders():
    order = mongo.db.order

    result = []

    for q in order.find():
        result.append({'service': q['service'], 'operator': q['operator'], 'price': q['price']})

    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
