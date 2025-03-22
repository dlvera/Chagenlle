# schemas/__init__.py
from .tag import TagRead
from .comment import CommentRead
from .post import PostRead, PostCreateResponse
from .user import UserRead

# Reconstruir en orden ascendente de dependencias
TagRead.model_rebuild()            # 1. No depende de nadie
PostCreateResponse.model_rebuild() # 2. Depende de TagRead
PostRead.model_rebuild()           # 3. Depende de TagRead y CommentRead
CommentRead.model_rebuild()        # 4. Depende de UserRead y PostRead (ya reconstruidos)
UserRead.model_rebuild()           # 5. Depende de CommentRead (ya listo)

__all__ = ["UserRead", "PostRead", "CommentRead", "TagRead", "PostCreateResponse"]