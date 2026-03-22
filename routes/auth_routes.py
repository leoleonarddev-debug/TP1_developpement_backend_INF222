from flask import Blueprint, request, jsonify
from controllers.auth_controller import register, login

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register_route():
    """
    Créer un compte utilisateur
    ---
    tags:
      - Authentification
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: "johndoe"
            password:
              type: string
              example: "monMotDePasse123"
    responses:
      201:
        description: Utilisateur créé
      400:
        description: Données manquantes
      409:
        description: Utilisateur déjà existant
    """
    data = request.get_json()
    response, status_code = register(data)
    return jsonify(response), status_code


@auth_bp.route("/login", methods=["POST"])
def login_route():
    """
    Se connecter et obtenir un token JWT
    ---
    tags:
      - Authentification
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: "johndoe"
            password:
              type: string
              example: "monMotDePasse123"
    responses:
      200:
        description: Connexion réussie, token retourné
      401:
        description: Mot de passe incorrect
      404:
        description: Utilisateur introuvable
    """
    data = request.get_json()
    response, status_code = login(data)
    return jsonify(response), status_code
