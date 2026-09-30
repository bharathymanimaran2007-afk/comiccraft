import os
import re
from pathlib import Path

from diffusers import StableDiffusionPipeline
import torch

MODEL_ID = "runwayml/stable-diffusion-v1-5"
OUTPUT_DIR = Path("static/panels")
_pipeline = None


def _get_pipeline():
    global _pipeline
    if _pipeline is not None:
        return _pipeline

    token = os.getenv("HF_API_KEY") or os.getenv("HUGGINGFACE_TOKEN")
    kwargs = {}
    if token:
        kwargs["token"] = token

    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    _pipeline = StableDiffusionPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=dtype,
        **kwargs,
    )
    if torch.cuda.is_available():
        _pipeline = _pipeline.to("cuda")
    else:
        _pipeline = _pipeline.to("cpu")
    return _pipeline


def _safe_filename(prompt: str, index: int | None = None) -> str:
    prefix = f"panel_{index}_" if index is not None else "panel_"
    safe = re.sub(r"[^a-zA-Z0-9_-]+", "_", prompt[:55]).strip("_")
    return f"{prefix}{safe or 'comic'}.png"


def generate_image(image_prompt: str, panel_number: int | None = None) -> str:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pipeline = _get_pipeline()

    full_prompt = (
        f"{image_prompt}, comic book illustration, clear composition, "
        "consistent character design, expressive faces, detailed background"
    )
    image = pipeline(full_prompt, num_inference_steps=25).images[0]

    filename = _safe_filename(image_prompt, panel_number)
    path = OUTPUT_DIR / filename
    image.save(path)

    return f"/static/panels/{filename}"
