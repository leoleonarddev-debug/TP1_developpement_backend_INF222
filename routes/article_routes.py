from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from controllers.article_controller import (
    add_article, fetch_all_articles, fetch_article_by_id,
    modify_article, remove_article, search_articles_controller
)

article_bp = Blueprint("articles", __name__, url_prefix="/api/articles")


@article_bp.route("", methods=["POST"])
@jwt_required()
def create():
    """
    Créer un nouvel article
    ---
    tags:
      - Articles
    security:
      - Bearer: []
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - titre
            - contenu
            - auteur
          properties:
            titre:
              type: string
              example: "Mon premier article"
            contenu:
              type: string
              example: "Contenu de l'article..."
            auteur:
              type: string
              example: "Jean Dupont"
            categorie:
              type: string
              example: "Tech"
            tags:
              type: string
              example: "python, flask, api"
    responses:
      201:
        description: Article créé avec succès
      400:
        description: Données invalides
      401:
        description: Non authentifié
    """
    data = request.get_json()
    response, status_code = add_article(data)
    return jsonify(response), status_code


@article_bp.route("", methods=["GET"])
def get_all():
    """
    Récupérer tous les articles (avec filtres optionnels)
    ---
    tags:
      - Articles
    parameters:
      - in: query
        name: categorie
        type: string
        description: Filtrer par catégorie
      - in: query
        name: auteur
        type: string
        description: Filtrer par auteur
      - in: query
        name: date
        type: string
        description: Filtrer par date (format YYYY-MM-DD)
    responses:
      200:
        description: Liste des articles
    """
    categorie = request.args.get("categorie")
    auteur    = request.args.get("auteur")
    date      = request.args.get("date")

    response, status_code = fetch_all_articles(categorie=categorie, auteur=auteur, date=date)
    return jsonify(response), status_code


@article_bp.route("/search", methods=["GET"])
def search():
    """
    Rechercher des articles par texte
    ---
    tags:
      - Articles
    parameters:
      - in: query
        name: query
        type: string
        required: true
        description: Texte à rechercher dans le titre ou le contenu
    responses:
      200:
        description: Articles correspondant à la recherche
      400:
        description: Paramètre query manquant
    """
    query_text = request.args.get("query", "")
    response, status_code = search_articles_controller(query_text)
    return jsonify(response), status_code


@article_bp.route("/<int:article_id>", methods=["GET"])
def get_one(article_id):
    """
    Récupérer un article par son ID
    ---
    tags:
      - Articles
    parameters:
      - in: path
        name: article_id
        type: integer
        required: true
    responses:
      200:
        description: Article trouvé
      404:
        description: Article introuvable
    """
    response, status_code = fetch_article_by_id(article_id)
    return jsonify(response), status_code


@article_bp.route("/<int:article_id>", methods=["PUT"])
@jwt_required()
def update(article_id):
    """
    Modifier un article existant
    ---
    tags:
      - Articles
    security:
      - Bearer: []
    parameters:
      - in: path
        name: article_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          properties:
            titre:
              type: string
            contenu:
              type: string
            auteur:
              type: string
            categorie:
              type: string
            tags:
              type: string
    responses:
      200:
        description: Article mis à jour
      404:
        description: Article introuvable
    """
    data = request.get_json()
    response, status_code = modify_article(article_id, data)
    return jsonify(response), status_code


@article_bp.route("/<int:article_id>", methods=["DELETE"])
@jwt_required()
def delete(article_id):
    """
    Supprimer un article
    ---
    tags:
      - Articles
    security:
      - Bearer: []
    parameters:
      - in: path
        name: article_id
        type: integer
        required: true
    responses:
      200:
        description: Article supprimé
      404:
        description: Article introuvable
    """
    response, status_code = remove_article(article_id)
    return jsonify(response), status_code
