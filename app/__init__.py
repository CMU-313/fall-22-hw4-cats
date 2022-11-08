from flask import Flask

app = Flask(__name__)
app = Flask('fall-22-hw4-cats')
app = Flask(__name__.split('.')[0])

from app.handlers import routes