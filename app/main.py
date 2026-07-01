from fastapi import FastAPI
import os

from app.routes.health import router as health_router
from app.routes.secure import router as secure_router

APP_BASE_PATH = os.getenv("APP_BASE_PATH", "/")

app = FastAPI(title="Rodel App Root")
internal_app = FastAPI(title="Rodel App")

internal_app.include_router(health_router)
internal_app.include_router(secure_router)

# montaje dinámico (igual que stocks)
if APP_BASE_PATH and APP_BASE_PATH != "/":
    app.mount(APP_BASE_PATH, internal_app)
else:
    app.mount("/", internal_app)

