from fastapi import Depends, Request
from fastapi_admin.depends import get_current_admin, get_resources
from fastapi_admin.routes import router
from fastapi_admin.template import templates


@router.get("/", dependencies=[Depends(get_current_admin)])
async def home(
        request: Request,
        resources=Depends(get_resources),
):
    return templates.TemplateResponse(
        "layout.html",
        context={
            "request": request,
            "resources": resources,
            "resource_label": "Dashboard",
            "page_pre_title": "overview",
            "page_title": "Dashboard",
        },
    )