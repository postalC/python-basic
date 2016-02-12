################################################################################
# Social Buzz Clustering
# - Flask Server & simple API -
#
# Author <a href='mailto:wei.tah.chai@sap.com'>Chai Wei Tah</a>
# Copyright (C) 2015 by MLI SG SAP Inc.
################################################################################

# -- Load library --
from flask import Flask
from flask import request
from flask import json
from flask import jsonify
from ml import getClassify
from ml import getClassifies
import log

__copyright__ = "Copyright (C) 2015 MLI SG SAP Inc."
__license__ = "MLI SG SAP"
__version__ = "0.1.0"

logger = log.setup_custom_logger('root')
logger.info('Starting Server')

# -- Init --
app = Flask(__name__)


# -- Root Path --
@app.route("/")
def index():
    return "Social Buzz!"


# -- Single Message Get --
# here we want to get the value of input (i.e. ?input=some-value)
@app.route('/message')
def data():
    result = getClassify(request.args.get('id'), request.args.get('input'))
    resp = jsonify(result)
    resp.status_code = 200
    return resp


# -- Multiple Messages Post --
@app.route('/messages', methods=['POST'])
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
def not_found(code=None, error=None):
    if code and not code.isspace():
        message = {
            'status': code,
            'message': error
        }
    else:
        code = 404
        message = {
            'status': 404,
            'message': 'Not Found: ' + request.url
        }
    resp = jsonify(message)
    resp.status_code = code
    return resp


# -- Main --
if __name__ == '__main__':
    app.run(host='0.0.0.0')
