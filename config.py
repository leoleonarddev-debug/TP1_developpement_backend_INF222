import os

class Config:
    # ─── Base de données MySQL ───────────────────────────────────────────────
    MYSQL_HOST     = os.environ.get("MYSQL_HOST",     "localhost")
    MYSQL_USER     = os.environ.get("MYSQL_USER",     "flask_user")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "flask_pass")
    MYSQL_DB       = os.environ.get("MYSQL_DB",       "blog_db")

    # ─── Sécurité JWT ────────────────────────────────────────────────────────
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "super-secret-key-inf222-taf1-2026")
    SECRET_KEY     = os.environ.get("SECRET_KEY",     "secret-key-inf222-taf1-2026-blog")