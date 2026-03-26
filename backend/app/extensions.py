from __future__ import annotations

from flask_sock import Sock
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base, session_options={"expire_on_commit": False})
migrate = Migrate()
jwt = JWTManager()
sock = Sock()
