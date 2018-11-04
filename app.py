from flask import Flask, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'api_db'
app.config['MONGO_URI'] = 'mongodb://db:27017/api_db'

mongo = PyMongo(app)


@app.route('/')
def start():
    return 'Hello babe!'


# Return all orders
@app.route('/order')
def get_all_orders():
    order = mongo.db.order

    result = []

    for q in order.find():
        result.append({'service': q['service'], 'operator': q['operator'], 'cost': q['cost'], 'ts': q['ts']})

    return jsonify({'result': result})


# Return order
@app.route('/order/<service>')
def get_one_user(service):
    order = mongo.db.order

    q = order.find_one({'ts': service})

    if q:
        result = {'service': q['service'], 'operator': q['operator'], 'cost': q['cost'], 'ts': q['ts']}
    else:
        result = 'No results found'

    return jsonify({'result': result})


# Add order
@app.route('/order/add/<service>/<operator>/<cost>/<ts>')
def add_order(service, operator, cost, ts):
    order = mongo.db.order

    order.insert({'service': service, 'operator': operator, 'cost': cost, 'ts': ts})

    return 'Order added!'


# Delete order
@app.route('/order/delete/<service>')
def delete_user(service):
    order = mongo.db.order

    order.delete_one({'service': service})

    return 'Order deleted!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
