import os

from jinja2 import ChoiceLoader,FileSystemLoader

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.permissions import (
    resolve_context,
    get_context_info,
)

APP_TEMPLATES_DIR = os.getenv("APP_TEMPLATES_DIR")
BAPP_TEMPLATE_DIR = "app/templates"

router = APIRouter()
templates = Jinja2Templates(directory=".")

templates.env.loader = ChoiceLoader([
    FileSystemLoader(APP_TEMPLATES_DIR),
    FileSystemLoader(BAPP_TEMPLATE_DIR),
])


@router.get("/", response_class=HTMLResponse)
def home(request: Request):

    app_id, client_id = resolve_context(
        request=request,
        x_app_id=None,
        x_client_id=None,
    )

    context_info = get_context_info(
        request=request,
        app_id=app_id,
        client_id=client_id,
    )

    return templates.TemplateResponse(
        request=request,
        name="shell_template.html",
        context={
            "app_name": context_info.get("app_name"),
            "app_id": app_id,
            "client_id": client_id,
            "context_info": context_info,
            "base_path": request.scope.get("root_path", ""),
            "username": context_info.get("user"),
            
            "menu_header_template": "menu_header.html",
            "menu_body_template": "menu_body.html",
            "content_template": "content.html",
        },
    )