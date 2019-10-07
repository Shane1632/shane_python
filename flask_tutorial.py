from flask import Flask, jsonify,request, render_template

app = Flask(__name__)

# Create a variable list for a JSON store
stores = [
    {
        'name': 'My Magical Store',
        'items' : [
            {
                'name': 'Product 1',
                'price' : 15.95
            },
            {
                'name' : 'Product 2',
                'price' : 12.60
            }
        ]
    }
]


@app.route('/')
def home():
    return render_template('index.html')
# POST - used by us (the server here) to receive data
# GET - used by browser to send us data (So we send data back)

# Our endpoints will be
# POST /store data: {name:}  Create a new store with given {name:}
@app.route('/store', methods=['POST'])    # means new store POSTs need to go to localhost:5000/store
def create_store():
    data = request.get_json()
    new_store = {
        'name' : data['name'],
        'items' : []
    }
    stores.append(new_store)
    return jsonify(new_store)


# GET /store/<string:name>  Return data about a specific store
@app.route('/store/<string:name>')  # flask method for arguments eg. localhost:5000/store/some_name
def get_store(name):
    # iterate over stores
    # if name matches a store name, return it
    # if none match return error
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
        else:
            return jsonify({'Message' : 'Store not found'})


# GET /store  Return list of all the stores
@app.route('/store')
def get_store_list():
    # return stores  this will return a python list which javascript will not understand
    # it will understand a JSON string, so we can convert a python dictionary to JSON with jsonify
    # return jsonify(stores)  but stores is a python list not a dictionary, so we need to convert it
    # into a dictionary {'store_name' : stores} giving one key 'store_name' with a value= list of stores
    return jsonify( {'store_name' : stores})

# POST /store/<string:name>/item {name:, price:}    Create a new item inside a specific store
@app.route('/store/<string:name>/item', methods=['POST'])
def add_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name' : request_data['name'],
                'price' : request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(store)
    return jsonify({'Alert' : 'Store not found'})


# GET /store/<string:name>/item    Return all the items in a specific store
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'Items' : store['items']})
    return jsonify({'Alert' : 'No store found with that name'})



app.run(port=5000)