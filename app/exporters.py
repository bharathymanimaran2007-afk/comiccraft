from pathlib import Path
from datetime import datetime
from fpdf import FPDF
from PIL import Image
import re

EXPORT_DIR = Path("static/exports")


def _absolute_image_path(web_path: str) -> str:
    return web_path.lstrip("/").replace("/", str(Path("/").anchor))


def save_pdf(layout: list[dict]) -> str:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"comiccraft_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    output = EXPORT_DIR / filename

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in layout:
        pdf.add_page()
        pdf.set_font("Arial", "B", 18)
        pdf.multi_cell(0, 10, f"Panel {panel['panel_number']}: {panel['title']}")

        image_path = Path(panel["image_path"].lstrip("/"))
        if image_path.exists():
            with Image.open(image_path) as img:
                w, h = img.size
                max_w, max_h = 180, 105
                scale = min(max_w / w, max_h / h)
                iw, ih = w * scale, h * scale
            pdf.image(str(image_path), x=15, y=35, w=iw, h=ih)

        pdf.ln(110)
        pdf.set_font("Arial", "I", 11)
        pdf.multi_cell(0, 7, panel["scene_description"])

        pdf.ln(4)
        pdf.set_font("Arial", "B", 11)
        pdf.multi_cell(0, 7, "Caption")
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 7, panel["caption"])

        pdf.ln(3)
        pdf.set_font("Arial", "B", 11)
        pdf.multi_cell(0, 7, "Narration")
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 7, panel["narration"])

    pdf.output(str(output))
    return f"/static/exports/{filename}"
