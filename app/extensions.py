from flask_sqlalchemy import SQLAlchemy

__all__ = ("db", "Base")

# SQLAlchemy
db = SQLAlchemy()
Base = db.Model
