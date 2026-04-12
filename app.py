from flask import Flask
from routes.anime_endpoints import anime_bp

app = Flask(__name__)
app.register_blueprint(anime_bp)

if __name__ == "__main__":
    app.run(debug=True)