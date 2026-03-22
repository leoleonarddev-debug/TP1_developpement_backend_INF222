from models.user_model import create_user, get_user_by_username
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash


def register(data):
    """
    Inscrit un nouvel utilisateur après validation et hashage du mot de passe.
    """
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"error": "username et password sont obligatoires"}, 400

    existing = get_user_by_username(username)
    if existing:
        return {"error": "Cet utilisateur existe déjà"}, 409

    hashed_password = generate_password_hash(password)
    create_user(username, hashed_password)

    return {"message": "Utilisateur créé avec succès"}, 201


def login(data):
    """
    Authentifie un utilisateur et retourne un token JWT.
    """
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"error": "username et password sont obligatoires"}, 400

    user = get_user_by_username(username)

    if not user:
        return {"error": "Utilisateur introuvable"}, 404

    if not check_password_hash(user["password"], password):
        return {"error": "Mot de passe incorrect"}, 401

    # identity=str(...) pour être compatible avec les versions récentes de Flask-JWT
    token = create_access_token(identity=str(user["id"]))

    return {
        "message": "Connexion réussie",
        "access_token": token
    }, 200
