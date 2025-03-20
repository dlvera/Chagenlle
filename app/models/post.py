from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base
from .base import SoftDeleteQuery, TimestampMixin, SoftDeleteMixin, post_tag, Base


class Post(Base, TimestampMixin, SoftDeleteMixin):
    """Modelo de posts de blog"""
    __tablename__ = "posts"
    query_class = SoftDeleteQuery

    id = Column(Integer, primary_key=True, comment="ID único del post")
    title = Column(String(100), nullable=False, comment="Título del post")
    content = Column(String(2000), nullable=False, comment="Contenido del post")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), comment="ID del autor del post")

    # Relaciones
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    tags = relationship("Tag", secondary=post_tag, back_populates="posts")