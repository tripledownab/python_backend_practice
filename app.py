from flask import Flask, jsonify

app = Flask(__name__)

# Sample data
data = [
    {"id": 1, "name": "Item One", "category": "Category A"},
    {"id": 2, "name": "Item Two", "category": "Category B"}
]

@app.route("/")
def welcome():
    return "<h1>FA APIs</h1>"

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)