from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, Table, DateTime
from sqlalchemy.orm import declarative_base, Query

Base = declarative_base()

class TimestampMixin:
    """
    Mixin que añade campos de timestamp automáticos
    Campos añadidos:
        created_at (DateTime): Fecha de creación
        updated_at (DateTime): Fecha de última modificación
    """
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
        comment="Fecha y hora de creación del registro"
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        index=True,
        comment="Fecha y hora de última actualización del registro"
    )

class SoftDeleteMixin:
    """
    Mixin que añade funcionalidad de soft-delete
    Campos añadidos:
        deleted_at (DateTime): Marca de tiempo de eliminación (None si no está eliminado)
    """
    deleted_at = Column(
        DateTime, 
        nullable=True, 
        default=None, 
        comment="Fecha y hora de eliminación lógica (None=no eliminado)"
    )

    def delete(self):
        """Marca el registro como eliminado estableciendo la fecha actual"""
        self.deleted_at = datetime.utcnow()

    def undelete(self):
        """Restaura un registro eliminado estableciendo deleted_at a None"""
        self.deleted_at = None
        
# ------------------------------------------
#           QUERY PERSONALIZADO
# ------------------------------------------
class SoftDeleteQuery(Query):
    """
    Query personalizado para filtrar registros eliminados lógicamente por defecto
    Filtra automáticamente registros no eliminados"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._query = self._query.filter(SoftDeleteMixin.deleted_at == None)  # ✅ Filtro activo
        
        
# ------------------------------------------
#          TABLA DE ASOCIACIÓN
# ------------------------------------------
post_tag = Table(
    "post_tag",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id"), comment="ID del post"),
    Column("tag_id", Integer, ForeignKey("tags.id"), comment="ID del tag"),
)