from flask import Flask

app = Flask(__name__)

if __name__ == "__main__":
    app.config['SECRET_KEY'] = os.environ['TOKEN']
    app.run(debug=True, port=os.getenv("PORT", default=5000))
