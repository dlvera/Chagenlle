from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from .base import SoftDeleteQuery, TimestampMixin, SoftDeleteMixin, post_tag, Base


class Tag(Base, TimestampMixin, SoftDeleteMixin):
    """Modelo de etiquetas para categorizar posts"""
    __tablename__ = "tags"
    query_class = SoftDeleteQuery

    id = Column(Integer, primary_key=True, comment="ID único de la etiqueta")
    name = Column(String(30), unique=True, nullable=False, comment="Nombre de la etiqueta")

    # Relaciones
    posts = relationship("Post", secondary=post_tag, back_populates="tags")