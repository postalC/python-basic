from flask import Flask

app = Flask(__name__)

import logging
file_handler = logging.FileHandler('app.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

# -- Root Path --
@app.route("/")
def hello():
    return "Social Buzz!"


# -- Single Message Get --
from flask import request
from flask import json
from flask import jsonify
from ml import getClassify
from ml import getClassifies
@app.route('/message')
def data():
    # here we want to get the value of input (i.e. ?input=some-value)
    result = getClassify(request.args.get('input'))
    app.logger.info(result)
    resp = jsonify(result)
    resp.status_code = 200
    return resp


# -- Multiple Messages Post --
@app.route('/messages', methods = ['POST'])
def api_message():
    if request.headers['Content-Type'] == 'application/json':
        result = getClassifies(json.dumps(request.json))
        resp = jsonify(result)
        resp.status_code = 200
        return resp
    else:
       return not_found()


# -- Error Message --
@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0')