from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.models.post import Post
from app.models.tag import Tag
from app.models.user import User
from app.schemas.post import PostCreate, PostCreateResponse, PostRead 
from app.utils.security import get_current_user, get_db
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=PostCreateResponse)
async def create_post(
    post: PostCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        new_post = Post(
            title=post.title,
            content=post.content,
            user_id=current_user.id
        )
        
        # Manejo de tags con mejor gestión de errores
        if not post.tags:
            result = await db.execute(select(Tag).where(Tag.name == "General"))
            default_tag = result.scalars().first()
            
            if not default_tag:
                raise HTTPException(
                    status_code=404,
                    detail="Tag por defecto no encontrado",
                    headers={"X-Error": "Database Error"}
                )
            new_post.tags = [default_tag]
        else:
            # Validación más robusta de tags
            result = await db.execute(
                select(Tag).where(Tag.id.in_(post.tags))
            )
            tags = result.scalars().all()
            
            if len(tags) != len(post.tags):
                raise HTTPException(
                    status_code=404,
                    detail="Algunos tags no fueron encontrados",
                    headers={"X-Error": "Invalid Tags"}
                )
            new_post.tags = tags
        
        # Manejo de la sesión con transacción
        db.add(new_post)
        await db.commit()
        
        # Refrescar el objeto con las relaciones
        await db.refresh(new_post)
        await db.execute(
            select(Post)
            .where(Post.id == new_post.id)
            .options(selectinload(Post.tags))
        )
        
        return new_post
        
    except Exception as e:
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

@router.put("/{post_id}", response_model=PostRead)
async def update_post(
    post_id: int,
    post: PostCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        # Primero, cargar el post con sus relaciones
        result = await db.execute(
            select(Post)
            .where(Post.id == post_id)
            .options(
                selectinload(Post.tags),
                selectinload(Post.user)
            )
        )
        db_post = result.scalars().first()
        
        if not db_post:
            raise HTTPException(status_code=404, detail="Post not found")
            
        if db_post.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this post")
            
        # Actualizar el contenido
        db_post.title = post.title
        db_post.content = post.content
        
        # Manejar tags si se proporcionan
        if post.tags:
            result = await db.execute(
                select(Tag).where(Tag.id.in_(post.tags))
                .options(selectinload(Tag.posts))
            )
            db_post.tags = result.scalars().all()
        
        await db.commit()
        
        # Recargar el post con todas las relaciones
        result = await db.execute(
            select(Post)
            .where(Post.id == db_post.id)
            .options(
                selectinload(Post.tags),
                selectinload(Post.user)
            )
        )
        return result.scalars().first()
        
    except Exception as e:
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

@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Post).where(Post.id == post_id))
    db_post = result.scalars().first()
    
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    
    db_post.delete()    # Para eliminación física
    await db.commit()
    return {"message": "Post deleted successfully"}

@router.get("/", response_model=List[PostRead])
async def read_posts(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Post)
        .where(Post.deleted_at == None)  # Filtra posts no eliminados
        .order_by(Post.created_at.desc())  # ¡Orden obligatorio!
        .offset(skip)
        .limit(limit)
        .options(selectinload(Post.tags),
                 selectinload(Post.user))  # Cargar relaciones
    )
    posts = result.scalars().all()
    return posts

# En el endpoint read_post
@router.get("/{post_id}", response_model=PostRead)
async def read_post(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Post)
        .where(Post.deleted_at == None)  # Filtra posts no eliminados
        .options(selectinload(Post.tags), 
                 selectinload(Post.user))  # Cargar relaciones
    )
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post