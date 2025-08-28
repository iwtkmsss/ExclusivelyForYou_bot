from pathlib import Path
import os
import json
import random

base_dir = Path(Path(__file__).parent)


async def get_random_recipe(category: str = None) -> dict:
    """
    :param category:
    :return: {content: str, video: Path}
    """
    subdirectories = [item for item in base_dir.iterdir() if item.is_dir()]

    if category:
        category_path = Path(base_dir, category)
        category_name = category
    else:
        category_path = random.choice(subdirectories)
        category_name = os.path.basename(category_path)

    with open(Path(base_dir, "setting.json"), "r", encoding="utf-8") as f:
        setting = json.load(f)
    used = setting["used"].get(category_name, [])

    all_files = os.listdir(category_path)
    available_item = [file for file in all_files if file not in used]

    if not available_item:
        used = []
        available_item = all_files

    selected_item = random.choice(available_item)

    used.append(selected_item)
    setting["used"][category_name] = used

    with open(Path(base_dir, "setting.json"), "w", encoding="utf-8") as f:
        json.dump(setting, f, indent=4) # type: ignore[arg-type]

    txt_file = next((file for file in os.listdir(Path(category_path, selected_item)) if file.endswith('.txt')), None)
    with open(Path(category_path, selected_item, txt_file), "r", encoding="utf-8") as f:
        content = f.read()

    video = next((file for file in os.listdir(Path(category_path, selected_item)) if file.endswith('.mp4')), None)
    return {"content": content, "video": Path(category_path, selected_item, video)}


async def get_status_category() -> dict:
    with open(Path(base_dir, "setting.json"), "r", encoding="utf-8") as f:
        setting = json.load(f)
    used = setting["used"]
    data = {}

    subdirectories = [item for item in base_dir.iterdir() if item.is_dir()][:-1]
    for s in subdirectories:
        category_name = os.path.basename(s)
        all_files = os.listdir(s)
        used_files = used.get(category_name, [])
        available_files = [file for file in all_files if file not in used_files]
        data[category_name] = available_files

    return data
