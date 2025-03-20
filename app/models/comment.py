from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from .base import SoftDeleteQuery, TimestampMixin, SoftDeleteMixin, Base



class Comment(Base, TimestampMixin, SoftDeleteMixin):
    """Modelo de comentarios en posts"""
    __tablename__ = "comments"
    query_class = SoftDeleteQuery

    id = Column(Integer, primary_key=True, comment="ID único del comentario")
    content = Column(String(500), nullable=False, comment="Texto del comentario")
    user_id = Column(Integer, ForeignKey("users.id"), comment="ID del usuario autor")
    post_id = Column(Integer, ForeignKey("posts.id"), comment="ID del post relacionado")

    # Relaciones
    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")