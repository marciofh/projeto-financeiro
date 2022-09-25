from flask import Flask, request, json
import calculator as c
app = Flask(__name__)

@app.route('/add_document', methods=['POST'])
def hello_world():
    doc = request.json['document']
    doc = json.dumps(doc)
    c.read_document(doc)
    return '200'

@app.route('/', methods=['GET'])
def hello():
    return 'doc'

if __name__ == '__main__':
    app.run()


