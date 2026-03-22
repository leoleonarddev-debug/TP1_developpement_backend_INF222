# 📚 Blog API — INF222 EC1 TAF1

API REST Flask pour la gestion d'un blog avec authentification JWT.

---

## 🏗️ Structure du projet

```
blog_api/
├── app.py                    # Point d'entrée de l'application
├── config.py                 # Configuration (DB, JWT, etc.)
├── database/
│   ├── db.py                 # Connexion MySQL
│   └── init.sql              # Script SQL de création des tables
├── models/
│   ├── article_model.py      # Requêtes SQL pour les articles
│   └── user_model.py         # Requêtes SQL pour les utilisateurs
├── controllers/
│   ├── article_controller.py # Logique métier des articles
│   └── auth_controller.py    # Logique d'authentification
├── routes/
│   ├── article_routes.py     # Endpoints /api/articles
│   └── auth_routes.py        # Endpoints /api/auth
├── schemas/
│   └── article_schema.py     # Validation Marshmallow
└── frontend/
    ├── index.html
    ├── style.css
    └── app.js
```

---

## ⚙️ Installation

### 1. Prérequis
- Python 3.8+
- MySQL

### 2. Cloner le dépôt
```bash
git clone https://github.com/votre-username/blog-api-inf222.git
cd blog-api-inf222
```

### 3. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 4. Installer les dépendances
```bash
pip install flask flask-jwt-extended flask-cors flask-mysqldb marshmallow flasgger mysql-connector-python werkzeug
```

### 5. Initialiser la base de données
```bash
mysql -u root -p < database/init.sql
```

### 6. Configurer les variables d'environnement (optionnel)
```bash
export MYSQL_HOST=localhost
export MYSQL_USER=flask_user
export MYSQL_PASSWORD=flask_pass
export MYSQL_DB=blog_db
export JWT_SECRET_KEY=ma-cle-secrete
```

### 7. Lancer l'application
```bash
python app.py
```

L'API est disponible sur `http://127.0.0.1:5000`

---

## 📖 Documentation Swagger

Accéder à la documentation interactive :
```
http://127.0.0.1:5000/api/docs
```

---

## 🔌 Endpoints

### Authentification

| Méthode | Endpoint             | Description                  | Auth requise |
|---------|----------------------|------------------------------|:------------:|
| POST    | `/api/auth/register` | Créer un compte              | ❌           |
| POST    | `/api/auth/login`    | Se connecter (retourne JWT)  | ❌           |

### Articles

| Méthode | Endpoint                         | Description                        | Auth requise |
|---------|----------------------------------|------------------------------------|:------------:|
| POST    | `/api/articles`                  | Créer un article                   | ✅           |
| GET     | `/api/articles`                  | Lister tous les articles           | ❌           |
| GET     | `/api/articles?categorie=Tech`   | Filtrer par catégorie              | ❌           |
| GET     | `/api/articles?auteur=Jean`      | Filtrer par auteur                 | ❌           |
| GET     | `/api/articles?date=2026-03-21`  | Filtrer par date                   | ❌           |
| GET     | `/api/articles/{id}`             | Récupérer un article par ID        | ❌           |
| PUT     | `/api/articles/{id}`             | Modifier un article                | ✅           |
| DELETE  | `/api/articles/{id}`             | Supprimer un article               | ✅           |
| GET     | `/api/articles/search?query=xxx` | Rechercher dans titre et contenu   | ❌           |

---

## 💡 Exemples d'utilisation

### Créer un compte
```bash
curl -X POST http://127.0.0.1:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "jean", "password": "motdepasse"}'
```

### Se connecter
```bash
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "jean", "password": "motdepasse"}'
```
Réponse : `{"access_token": "eyJ..."}`

### Créer un article
```bash
curl -X POST http://127.0.0.1:5000/api/articles \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ..." \
  -d '{
    "titre": "Mon premier article",
    "contenu": "Contenu de l article",
    "auteur": "Jean",
    "categorie": "Tech",
    "tags": "python, flask"
  }'
```

### Rechercher un article
```bash
curl "http://127.0.0.1:5000/api/articles/search?query=python"
```

---

## ✅ Codes HTTP utilisés

| Code | Signification             |
|------|---------------------------|
| 200  | Succès                    |
| 201  | Création réussie          |
| 400  | Requête invalide          |
| 401  | Non authentifié           |
| 404  | Ressource introuvable     |
| 409  | Conflit (déjà existant)   |
| 500  | Erreur serveur            |
