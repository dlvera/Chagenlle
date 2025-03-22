# Orden correcto (dependencias primero):
from .tag import TagRead
from .comment import CommentRead
from .post import PostRead, PostCreateResponse
from .user import UserRead

# Reconstruir en este orden:
CommentRead.model_rebuild()        # 1. Depende de UserRead y PostRead (aún no reconstruidos)
TagRead.model_rebuild()            # 2. Depende de PostRead
PostRead.model_rebuild()           # 3. Depende de TagRead y CommentRead (ya listos)
UserRead.model_rebuild()           # 4. Depende de CommentRead y PostRead
PostCreateResponse.model_rebuild() # 5. Depende de TagRead (ya listo)