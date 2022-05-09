from app import app
import os

if __name__ == "__main__":
    app.config['SECRET_KEY'] = os.environ['TOKEN']

    app.run(debug=True)
