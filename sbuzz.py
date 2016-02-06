from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/data')
def data():
    # here we want to get the value of user (i.e. ?user=some-value)
    user = request.args.get('user')
    return "your input " + user


if __name__ == '__main__':
    app.run(host='0.0.0.0')