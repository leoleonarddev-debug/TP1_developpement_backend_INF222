from database.db import get_db

# ─────────────────────────────────────────────────────────────────────────────
# BUGS CORRIGÉS :
#   1. INSERT : virgule manquante entre %s (%s,%s,%s,%s.%s  →  %s,%s,%s,%s,%s)
#   2. INSERT : "catagorie" (faute d'orthographe) → "categorie"
#   3. INSERT : db.commit() et cursor.close() absents après l'insertion
#   4. create_article() ne retournait pas l'ID de l'article créé
#   5. search_articles() ne cherchait que dans le titre, ajout du contenu
# ─────────────────────────────────────────────────────────────────────────────

def create_article(data):
    """
    Insère un nouvel article en base et retourne son ID.
    """
    db = get_db()
    cursor = db.cursor()

    # BUG CORRIGÉ : virgule manquante entre le 4e et 5e %s
    query = """
    INSERT INTO article (titre, contenu, auteur, categorie, tags)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        data["titre"],
        data["contenu"],
        data["auteur"],
        data.get("categorie", "General"),   # BUG CORRIGÉ : "catagorie" → "categorie"
        data.get("tags", "")
    ))

    db.commit()                  # BUG CORRIGÉ : commit absent
    article_id = cursor.lastrowid  # BUG CORRIGÉ : retourner l'ID

    cursor.close()
    db.close()

    return article_id


def get_all_articles(categorie=None, auteur=None, date=None):
    """
    Retourne tous les articles, avec filtres optionnels.
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)

    query  = "SELECT * FROM article WHERE 1=1"
    params = []

    if categorie:
        query += " AND categorie = %s"
        params.append(categorie)

    if auteur:
        query += " AND auteur = %s"
        params.append(auteur)

    if date:
        query += " AND DATE(created_at) = %s"
        params.append(date)

    query += " ORDER BY created_at DESC"

    cursor.execute(query, params)
    articles = cursor.fetchall()

    cursor.close()
    db.close()

    return articles


def get_article_by_id(article_id):
    """
    Retourne un article par son ID, ou None s'il n'existe pas.
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM article WHERE id = %s", (article_id,))
    article = cursor.fetchone()

    cursor.close()
    db.close()

    return article


def update_article(article_id, data):
    """
    Met à jour un article existant. Retourne le nombre de lignes affectées.
    """
    db = get_db()
    cursor = db.cursor()

    query = """
    UPDATE article
    SET titre     = %s,
        contenu   = %s,
        auteur    = %s,
        categorie = %s,
        tags      = %s
    WHERE id = %s
    """
    values = (
        data.get("titre"),
        data.get("contenu"),
        data.get("auteur"),
        data.get("categorie"),
        data.get("tags"),
        article_id
    )

    cursor.execute(query, values)
    db.commit()

    affected_rows = cursor.rowcount

    cursor.close()
    db.close()

    return affected_rows


def delete_article(article_id):
    """
    Supprime un article par son ID. Retourne le nombre de lignes affectées.
    """
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM article WHERE id = %s", (article_id,))
    db.commit()

    affected_rows = cursor.rowcount

    cursor.close()
    db.close()

    return affected_rows


def search_articles(query):
    """
    Recherche des articles dont le titre OU le contenu contient le texte donné.
    BUG CORRIGÉ : la recherche couvrait uniquement le titre.
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)

    sql = "SELECT * FROM article WHERE titre LIKE %s OR contenu LIKE %s"
    like_param = "%" + query + "%"
    cursor.execute(sql, (like_param, like_param))

    results = cursor.fetchall()

    cursor.close()
    db.close()

    return results


def get_articles_paginated(limit, offset):
    """
    Retourne une page d'articles (pour la pagination).
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM article ORDER BY created_at DESC LIMIT %s OFFSET %s",
        (limit, offset)
    )
    data = cursor.fetchall()

    cursor.close()
    db.close()

    return data
