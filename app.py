from flask import Flask, send_from_directory
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger
from config import Config
import os

# ─── Import des Blueprints ────────────────────────────────────────────────────
from routes.article_routes import article_bp
from routes.auth_routes import auth_bp

# ─── Initialisation ──────────────────────────────────────────────────────────
# static_folder="frontend" → Flask sert les fichiers HTML/CSS/JS depuis ce dossier
# Cela permet au localStorage d'être PARTAGÉ entre toutes les pages (même origine)
app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)

# ─── Configuration ────────────────────────────────────────────────────────────
app.config.from_object(Config)

# ─── Extensions ───────────────────────────────────────────────────────────────
jwt = JWTManager(app)

# ─── Swagger ──────────────────────────────────────────────────────────────────
swagger_config = {
    "headers": [],
    "specs": [{
        "endpoint":     "apispec",
        "route":        "/apispec.json",
        "rule_filter":  lambda rule: True,
        "model_filter": lambda tag: True,
    }],
    "static_url_path": "/flasgger_static",
    "swagger_ui":       True,
    "specs_route":      "/api/docs"
}

swagger_template = {
    "info": {
        "title":       "Blog API",
        "description": "API REST pour la gestion d'un blog — INF222 EC1 TAF1",
        "version":     "1.0.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type":        "apiKey",
            "name":        "Authorization",
            "in":          "header",
            "description": "JWT Authorization. Format : Bearer <token>"
        }
    }
}

Swagger(app, config=swagger_config, template=swagger_template)

# ─── Routes Frontend ──────────────────────────────────────────────────────────
@app.route("/")
def home():
    return send_from_directory("frontend", "signup.html")

@app.route("/signup")
def signup_page():
    return send_from_directory("frontend", "signup.html")

@app.route("/login")
def login_page():
    return send_from_directory("frontend", "login.html")

@app.route("/blog")
def blog_page():
    return send_from_directory("frontend", "index.html")

# ─── Routes API ───────────────────────────────────────────────────────────────
app.register_blueprint(auth_bp)
app.register_blueprint(article_bp)

# ─── Lancement ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)