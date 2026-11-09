from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.settings import settings

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Chat.com messaging platform API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    return {"service": "Chat.com API", "status": "online", "docs": "/docs"}


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "healthy", "service": "chat-com-api", "version": "0.1.0"}


@app.get(f"{settings.api_prefix}/system", tags=["system"])
def system_info() -> dict[str, str]:
    return {"name": settings.app_name, "version": "0.1.0", "environment": settings.app_env}
