from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from ..utils.auth import get_password_hash, verify_password
from .base import SoftDeleteQuery, TimestampMixin, SoftDeleteMixin, Base

class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"
    query_class = SoftDeleteQuery

    id = Column(Integer, primary_key=True, comment="ID único del usuario")
    username = Column(String(50), unique=True, nullable=False, comment="Nombre de usuario único")
    password_hash = Column(String(128), nullable=False, comment="Hash de la contraseña")

    # Métodos para contraseña
    def set_password(self, password: str):
        self.password_hash = get_password_hash(password)

    def check_password(self, password: str) -> bool:
        return verify_password(password, self.password_hash)

    # Relaciones
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")