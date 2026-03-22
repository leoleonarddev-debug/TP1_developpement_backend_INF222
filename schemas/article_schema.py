from marshmallow import Schema, fields, validate

class ArticleSchema(Schema):
    """
    Schéma de validation pour un article.
    Marshmallow vérifie automatiquement les types et les contraintes.
    """
    titre     = fields.Str(required=True,  validate=validate.Length(min=1, max=255))
    contenu   = fields.Str(required=True,  validate=validate.Length(min=1))
    auteur    = fields.Str(required=True,  validate=validate.Length(min=1, max=100))
    categorie = fields.Str(load_default="General")
    tags      = fields.Str(load_default="")
