from database.db import get_db

def create_user(username, password):
    """
    Insère un nouvel utilisateur en base.
    """
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO user (username, password) VALUES (%s, %s)",
        (username, password)
    )
    db.commit()

    cursor.close()
    db.close()


def get_user_by_username(username):
    """
    Retourne un utilisateur par son nom d'utilisateur, ou None.
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM user WHERE username = %s",
        (username,)
    )
    user = cursor.fetchone()

    cursor.close()
    db.close()

    return user
