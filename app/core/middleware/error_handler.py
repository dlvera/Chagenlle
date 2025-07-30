from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(SQLAlchemyError)
async def sql_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Error de base de datos"}
    )