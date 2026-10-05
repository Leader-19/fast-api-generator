from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.permissions import router as permissions_router
from app.api.roles import router as roles_router
from app.api.users import router as users_router
# from app.api.pdf_converter import router as pdf_converter_router
from app.api.pdf_converter import (
    router as pdf_converter_router,
)

from app.middleware.cors import register_cors_middleware


app = FastAPI(
    title="Roaming Reconciliation Portal API",
    version="1.0.0",
)

# middleware
register_cors_middleware(app)


# =========================
# API ROUTERS
# =========================

app.include_router(auth_router)
app.include_router(roles_router)
app.include_router(permissions_router)
app.include_router(users_router)
# app.include_router(pdf_converter_router)
app.include_router(
    pdf_converter_router
)


# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Roaming Reconciliation Portal API",
        "docs": "/docs",
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "message": "API is running",
    }