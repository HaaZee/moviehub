from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['TOKEN']

from app import routes
