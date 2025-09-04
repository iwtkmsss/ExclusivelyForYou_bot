import re
from pathlib import Path
import os
import json
import random

import requests
from bs4 import BeautifulSoup

base_dir = Path(Path(__file__).parent)


t_zodiac_signs = {
    "Leo": {"name": "Лева", "sign": "♌️"},
    "Aries": {"name": "Овна", "sign": "♈️"},
    "Gemini": {"name": "Близнюків", "sign": "♊️"},
    "Cancer": {"name": "Рака", "sign": "♋️"},
    "Taurus": {"name": "Тельця", "sign": "♉️"},
    "Virgo": {"name": "Діви", "sign": "♍️"},
    "Libra": {"name": "Терезів", "sign": "♎️"},
    "Scorpio": {"name": "Скорпіона", "sign": "♏️"},
    "Sagittarius": {"name": "Стрільця", "sign": "♐️"},
    "Capricorn": {"name": "Козерога", "sign": "♑️"},
    "Aquarius": {"name": "Водолія", "sign": "♒️"},
    "Pisces": {"name": "Риб", "sign": "♓️"}
}

async def get_random_premium_recipe(category: str = None) -> dict:
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


async def get_random_json_food(path):
    recipes_path = base_dir / path

    with open(recipes_path, "r", encoding="utf-8") as f:
        recipes = json.load(f)

    while True:
        key = random.choice(list(recipes.keys()))
        if not recipes[key].get("used"):
            recipes[key]["used"] = True
            break

    with open(recipes_path, "w", encoding="utf-8") as f:
        json.dump(recipes, f, ensure_ascii=False, indent=4) # type: ignore[arg-type]

    return recipes[key]


async def get_scraping_zodiac_sign(zodiac_sign) -> dict:
    url = "https://gosta.media/horoskop-na-sohodni/"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    }

    s = requests.Session()
    response = s.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    main_link = "https://gosta.media" + (soup.find("div", class_="container block-with-cols").find("a", class_="post-card").get('href'))

    response = s.get(url=main_link, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    h2 = soup.find("h2", string=re.compile(zodiac_sign))
    if h2:
        date_sign = h2.get_text(strip=True)  # "Гороскоп на 4 вересня 2025 року для Тельця"
        p = h2.find_next_sibling("p")  # первый параграф после h2
        text = p.get_text(" ", strip=True) if p else None

        result = {
            "title": date_sign,
            "text": text
        }
        return result
    return {}
