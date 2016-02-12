################################################################################
# Social Buzz Clustering
# - Flask Server & simple API -
#
# Author <a href='mailto:wei.tah.chai@sap.com'>Chai Wei Tah</a>
# Copyright (C) 2015 by MLI SG SAP Inc.
################################################################################

# -- Load library --
from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask import request
from flask import json
from flask import jsonify
from ml import getClassify
from ml import getClassifies
from database import db, Data
from sqlalchemy.orm import sessionmaker
from flask import url_for, redirect
from flask.ext.wtf import Form
from wtforms.fields import StringField, SubmitField
import random
import log

__copyright__ = "Copyright (C) 2015 MLI SG SAP Inc."
__license__ = "MLI SG SAP"
__version__ = "0.1.0"

logger = log.setup_custom_logger('root')
logger.info('Starting Server')

# -- Init --
app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = "t%Bh9mXe=YzWJh3fW8*v"

# -- Database Session --
Session = sessionmaker(bind=db)
session = Session()


# - Submit Form --
class SubmitForm(Form):
    message = StringField(u'message to classify:')
    submit = SubmitField(u'process')


# -- Root Path --
@app.route("/")
def index():
    result = session.query(Data).all()
    form = SubmitForm()
    return render_template('index.html', form=form, result=result)


# -- Simple Static Service - for DEMO ONLY --
@app.route('/static/<path:path>')
def sendstatic(path):
    return send_from_directory('static', path)


# -- Simple Form Submit --
@app.route('/new', methods=['POST'])
def newsubmit():
    form = SubmitForm()
    if form.validate_on_submit():
        submitted = Data()
        submitted.c4cid = random.random()
        form.populate_obj(submitted)
        result = getClassify(submitted.c4cid, submitted.message)
        print(result)
    return redirect(url_for('index'))


# -- Single Message Get --
# here we want to get the value of input (i.e. ?input=some-value)
@app.route('/message')
def getmessage():
    result = getClassify(request.args.get('id'), request.args.get('input'))
    resp = jsonify(result)
    resp.status_code = 200
    return resp


# -- Multiple Messages Post --
@app.route('/messages', methods=['POST'])
def postmessages():
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
