# ComicCraft - AI Comic Story Creator using Gemini Models

This project follows the supplied ComicCraft specification: FastAPI + Jinja2 frontend, Gemini Flash for a structured 5-panel outline, Gemini Pro for narration/dialogue, Stable Diffusion for comic illustrations, layout assembly, and FPDF PDF export.

## Project structure

```text
ComicCraft/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── gemini_flash.py
│   ├── gemini_pro.py
│   ├── image_generator.py
│   ├── layout_builder.py
│   └── exporters.py
├── templates/
│   ├── index.html
│   ├── comic_preview.html
│   └── export_success.html
├── static/
│   ├── style.css
│   ├── panels/
│   └── exports/
├── .env.example
├── requirements.txt
└── README.md
```

## Windows setup

```powershell
python -m venv comiccraft-env
comiccraft-env\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Put your Gemini API key and Hugging Face token in `.env`.

## Run

```powershell
uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

## Workflow

1. `/` collects story prompt, character name, setting, tone and art style.
2. `/generate` creates a 5-panel outline with Gemini Flash.
3. Gemini Pro expands the outline into captions and narration.
4. Stable Diffusion generates one image per panel.
5. `layout_builder.py` combines the story and images.
6. `exporters.py` creates a timestamped PDF in `static/exports`.
7. `/generate-comic/json` exposes the JSON API workflow.
8. `/test-image` provides direct image-generation testing.
9. `/export-success` displays the export confirmation page.

## Notes

The supplied specification names `models/gemini-1.5-flash`, `models/gemini-1.5-pro`, and `runwayml/stable-diffusion-v1-5`; this implementation keeps those model identifiers to follow the document. Availability of those model identifiers depends on the installed SDK/API account and provider availability.
