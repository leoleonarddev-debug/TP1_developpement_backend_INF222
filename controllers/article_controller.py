from models.article_model import (
    create_article, get_all_articles, get_article_by_id,
    update_article, delete_article, search_articles
)
from schemas.article_schema import ArticleSchema

# ─────────────────────────────────────────────────────────────────────────────
# BUGS CORRIGÉS :
#   1. add_article() était défini deux fois – la 2e définition écrasait la 1ère
#      On fusionne les deux en une seule fonction qui valide ET crée.
# ─────────────────────────────────────────────────────────────────────────────

schema = ArticleSchema()


def add_article(data):
    """
    Valide les données puis crée un nouvel article.
    Retourne (réponse_dict, code_HTTP).
    """
    # Validation via Marshmallow
    errors = schema.validate(data)
    if errors:
        return {"errors": errors}, 400

    article_id = create_article(data)

    return {
        "message": "Article créé avec succès",
        "id": article_id
    }, 201


def fetch_all_articles(categorie=None, auteur=None, date=None):
    """
    Retourne tous les articles, filtrés si besoin.
    """
    articles = get_all_articles(categorie=categorie, auteur=auteur, date=date)

    return {
        "message": "Liste des articles",
        "data": articles
    }, 200


def fetch_article_by_id(article_id):
    """
    Retourne un article par son ID ou une erreur 404.
    """
    article = get_article_by_id(article_id)

    if not article:
        return {"error": "Article introuvable"}, 404

    return {
        "message": "Article trouvé",
        "data": article
    }, 200


def modify_article(article_id, data):
    """
    Met à jour un article existant.
    """
    # Vérifier existence
    article = get_article_by_id(article_id)
    if not article:
        return {"error": "Article introuvable"}, 404

    updated = update_article(article_id, data)

    if updated == 0:
        return {"error": "Aucune modification effectuée"}, 400

    return {"message": "Article mis à jour avec succès"}, 200


def remove_article(article_id):
    """
    Supprime un article par son ID.
    """
    article = get_article_by_id(article_id)
    if not article:
        return {"error": "Article introuvable"}, 404

    deleted = delete_article(article_id)

    if deleted == 0:
        return {"error": "Suppression échouée"}, 400

    return {"message": "Article supprimé avec succès"}, 200


def search_articles_controller(query_text):
    """
    Recherche des articles par texte dans le titre ou le contenu.
    """
    if not query_text:
        return {"error": "Paramètre 'query' manquant"}, 400

    results = search_articles(query_text)

    return {
        "message": f"{len(results)} article(s) trouvé(s)",
        "data": results
    }, 200
