import json
import os

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

from .gemini_flash import generate_outline
from .gemini_pro import generate_story
from .image_generator import generate_image
from .layout_builder import build_comic_layout
from .exporters import save_pdf

router = APIRouter()


class PromptRequest(BaseModel):
    story_prompt: str = Field(min_length=1)
    character_name: str = Field(min_length=1)
    setting: str = Field(min_length=1)
    tone: str = Field(min_length=1)
    art_style: str = Field(min_length=1)


def _generate_comic(data: PromptRequest):
    outline = generate_outline(
        data.story_prompt,
        data.character_name,
        data.setting,
        data.tone,
        data.art_style,
    )
    story = generate_story(outline, data.character_name, data.tone)
    images = [
        generate_image(panel["image_prompt"], panel["panel_number"])
        for panel in outline
    ]
    layout = build_comic_layout(outline, story, images)
    pdf_path = save_pdf(layout)
    return layout, pdf_path


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return request.app.state.templates.TemplateResponse(
        "index.html", {"request": request}
    )


@router.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    try:
        layout, pdf_path = _generate_comic(
            PromptRequest(
                story_prompt=story_prompt,
                character_name=character_name,
                setting=setting,
                tone=tone,
                art_style=art_style,
            )
        )
        return request.app.state.templates.TemplateResponse(
            "comic_preview.html",
            {"request": request, "layout": layout, "pdf_path": pdf_path},
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/generate-comic/json")
async def generate_comic_json(payload: PromptRequest):
    try:
        layout, pdf_path = _generate_comic(payload)
        return JSONResponse({"layout": layout, "pdf_path": pdf_path})
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request):
    return request.app.state.templates.TemplateResponse(
        "export_success.html", {"request": request}
    )


@router.get("/test-image", response_class=JSONResponse)
async def test_image(prompt: str = "A brave fox exploring an enchanted forest, anime comic style"):
    try:
        path = generate_image(prompt)
        return {"image_path": path}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
