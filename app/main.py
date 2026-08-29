from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from app.routes.health import router as health_router
from app.routes.secure import router as secure_router
from app.routes.ui import router as ui_router
from app.core.startup import startup

APP_BASE_PATH = os.getenv("APP_BASE_PATH", "/")
RODELSOFT_APP = os.getenv("RODELSOFT_APP", "/")

app = FastAPI(title="rodelSoft Applications " + RODELSOFT_APP)
internal_app = FastAPI(title=RODELSOFT_APP)

@internal_app.on_event("startup")
def startup_event():
    startup()

internal_app.include_router(ui_router)
internal_app.include_router(health_router)
internal_app.include_router(secure_router)

internal_app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)

internal_app.mount(
    "/framework", 
    StaticFiles(directory="framework/static"), 
    name="framework"
)

# montaje dinámico (igual que stocks)
if APP_BASE_PATH and APP_BASE_PATH != "/":
    app.mount(APP_BASE_PATH, internal_app)
else:
    app.mount("/", internal_app)