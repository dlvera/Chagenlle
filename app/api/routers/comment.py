from fastapi import APIRouter, Depends, HTTPException, logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.schemas.comment import CommentBase, CommentCreate, CommentCreateResponse
from app.schemas import CommentRead
from app.models.post import Post
from app.models.comment import Comment
from app.models.tag import Tag
from app.models.user import User
from app.core.utils.security import get_current_user, get_db
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/comment", tags=["Comment"])

@router.post("/", response_model=CommentCreateResponse)
async def create_comment(
    comment: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        # Verificar si el usuario ya comentó este post
        existing_comment = await db.execute(
            select(Comment)
            .where(
                Comment.user_id == current_user.id,
                Comment.post_id == comment.post_id
            )
        )
        
        if existing_comment.scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail="Ya has comentado este post"
            )
        new_comment = Comment(
            content=comment.content,
            user_id=current_user.id,
            post_id=comment.post_id
        )
        
        db.add(new_comment)
        await db.commit()
        
        # Cargar relaciones necesarias
        result = await db.execute(
            select(Comment)
            .where(Comment.id == new_comment.id)
            .options(
                selectinload(Comment.post),
                selectinload(Comment.user)
            )
        )
        full_comment = result.scalar_one()
        
        # Convertir a Pydantic
        return CommentCreateResponse.model_validate(full_comment)
        
    except Exception as e:
        await db.rollback()  # ✅ Revierte la transacción en caso de error
        if "uix_user_post" in str(e):
            raise HTTPException(
                status_code=400,
                detail="Solo puedes comentar una vez por post"
            )
        # Manejo específico de errores
        if isinstance(e, HTTPException):
            raise e
        elif hasattr(e, "orig") and isinstance(e.orig, Exception):
            raise HTTPException(
                status_code=500,
                detail="Error en la base de datos",
                headers={"X-Error": str(e.orig)}
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="Error interno del servidor",
                headers={"X-Error": str(e)}
            )

@router.put("/{comment_id}", response_model=CommentRead)
async def update_comment(
    comment_id: int,
    comment: CommentBase,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        # Primero, cargar el commnet con sus relaciones
        result = await db.execute(
            select(Comment)
            .where(Comment.id == comment_id)
            .options(
               selectinload(Comment.user)
           )
        )
        db_comment = result.scalars().first()
        
        if not db_comment:
            raise HTTPException(status_code=404, detail="Comment not found")
            
        if db_comment.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this Comment")
            
        # Actualizar el contenido
        db_comment.content = comment.content
        
        await db.commit()
        
        # Recargar el comment con todas las relaciones
        result = await db.execute(
            select(Comment)
            .where(Comment.id == db_comment.id)
            .options(
                selectinload(Comment.user)
            )
        )
        return result.scalars().first()
        
    except Exception as e:
        await db.rollback()  # ✅ Revierte la transacción en caso de error
        if "uix_user_post" in str(e):
            raise HTTPException(
                status_code=400,
                detail="Solo puedes comentar una vez por post"
            )
        # Manejo específico de errores
        if isinstance(e, HTTPException):
            raise e
        elif hasattr(e, "orig") and isinstance(e.orig, Exception):
            raise HTTPException(
                status_code=500,
                detail="Error en la base de datos",
                headers={"X-Error": str(e.orig)}
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="Error interno del servidor",
                headers={"X-Error": str(e)}
            )

@router.delete("/{comment_id}")
async def delete_Commet(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    db_comment = result.scalars().first()
    
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this Comment")
    
    db_comment.delete()    # Para eliminación física
    await db.commit()
    return {"message": "Comment deleted successfully"}

@router.get("/", response_model=List[CommentRead])
async def read_comments(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Comment)
        .where(Comment.deleted_at == None)
        .order_by(Comment.created_at.desc())
        .offset(skip)
        .limit(limit)
        .options(
            selectinload(Comment.user),
            selectinload(Comment.post)
                .selectinload(Post.user)
                .selectinload(Post.tags),  # ✅ Cargar tags del post
)
    )
    comments = result.scalars().unique().all()
    return comments

@router.get("/{comment_id}", response_model=CommentRead)
async def read_comment(  # ✅ Nombre corregido
    comment_id: int, 
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Comment)
        .where(Comment.id == comment_id, Comment.deleted_at == None)
        .options(
            selectinload(Comment.user),
            selectinload(Comment.post).selectinload(Post.user),
        )
    )
    comment = result.scalars().first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    return comment
