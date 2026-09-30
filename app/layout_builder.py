def build_comic_layout(outline: list[dict], story: list[dict], image_paths: list[str]) -> list[dict]:
    story_by_panel = {item["panel_number"]: item for item in story}
    layout = []

    for panel, image_path in zip(outline, image_paths):
        story_item = story_by_panel.get(panel["panel_number"], {})
        layout.append({
            "panel_number": panel["panel_number"],
            "title": panel["title"],
            "image_path": image_path,
            "scene_description": panel["scene_description"],
            "image_prompt": panel["image_prompt"],
            "caption": story_item.get("caption", ""),
            "narration": story_item.get("narration", ""),
        })

    return layout
