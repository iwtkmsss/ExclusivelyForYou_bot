import base64
import re
from pathlib import Path
import os
import json
import random

import cairosvg
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


async def get_matrix_data(body):
    """
        body -: {"date1": "dd.mm.yyyy", "name1": "name", "gender": "m" || "f"}

        :param body:
        :return:
        """

    url = "https://matrix-doli.com/api/matrix/personal"
    s = requests.Session()
    body["purchase"] = False
    response = s.get(url=url, json=body).json()
    return response


async def chakra_matrix_html(data: dict) -> str:
    rows = [
        ("Сахасрара",   ("a","b","y1"),   "Місія",                         "7"),
        ("Аджна",       ("a1","b1","y2"), "Доля, егрегори",                "6"),
        ("Вішудха",     ("a2","b2","y3"), "Доля, егрегори",                "5"),
        ("Анахата",     ("a3","b3","y4"), "Відносини, картина світу",      "4"),
        ("Маніпура",    ("i","i","y5"),   "Статус, володіння",             "3"),
        ("Свадхістана", ("c2","d2","y6"), "Дитяче кохання та радість",     "2"),
        ("Муладхара",   ("c","d","y7"),   "Тіло, матерія",                  "1"),
        ("Підсумок",    ("y8","y9","y10"),"Загальне енергополе",           "—"),
    ]

    def fmt(n):
        return f"{n:>4}"

    lines = ["┌────────────────────────────────────┬────┬──────┬──────┐",
             "│ НАЙМЕНУВАННЯ ЧАКРИ                │ ФІЗ. │ ЕНЕРГ. │ ЕМОЦ. │",
             "├────────────────────────────────────┼────┼──────┼──────┤"]

    for title, (k1, k2, k3), subtitle, num in rows:
        v1, v2, v3 = data[k1], data[k2], data[k3]
        head = f"{num} {title}"
        sub  = subtitle
        # перший рядок: назва
        lines.append(f"│ {head:<34} │ {fmt(v1)} │ {fmt(v2)} │ {fmt(v3)} │")
        # другий рядок: підзаголовок (без чисел)
        lines.append(f"│ {sub:<34} │      │       │       │")
        lines.append("├────────────────────────────────────┼────┼──────┼──────┤")

    # заміна останнього роздільника на нижню рамку
    lines[-1] = "└────────────────────────────────────┴────┴──────┴──────┘"

    table = "\n".join(lines)

    return (
        f"<b>{data.get('title')}</b>\n\n"
        f"<pre>{table}</pre>"
    )


def _fix_opacity_percents(svg_text: str) -> str:
    # stroke-opacity="30%" | =30% | style="...opacity:30%;..."
    def repl_attr_q(m):  # with quotes
        name, q, num = m.group(1), m.group(2), m.group(3)
        return f'{name}={q}{float(num)/100:.6f}{q}'
    svg_text = re.sub(r'(?i)\b([a-z-]*opacity)\b\s*=\s*(["\'])(\d+(?:\.\d+)?)\s*%\s*\2',
                      repl_attr_q, svg_text)

    def repl_attr(m):  # no quotes
        name, num = m.group(1), m.group(2)
        return f'{name}="{float(num)/100:.6f}"'
    svg_text = re.sub(r'(?i)\b([a-z-]*opacity)\b\s*=\s*(\d+(?:\.\d+)?)\s*%',
                      repl_attr, svg_text)

    def repl_style(m):  # in style
        name, num, tail = m.group(1), m.group(2), m.group(3) or ''
        return f'{name}:{float(num)/100:.6f}{tail}'
    svg_text = re.sub(r'(?i)\b([a-z-]*opacity)\b\s*:\s*(\d+(?:\.\d+)?)\s*%(;)?',
                      repl_style, svg_text)
    return svg_text

def _fix_rem_to_px(svg_text: str, root_font_px: float = 16.0) -> str:
    # Переводимо будь-яке "<num>rem" → "<num*root>px"
    return re.sub(
        r'(?i)(-?\d+(?:\.\d+)?)\s*rem\b',
        lambda m: f'{float(m.group(1))*root_font_px:.6f}px',
        svg_text
    )

async def svg_b64_to_png_bytes(b64: str) -> bytes:
    # знімаємо префікс data:
    b64 = re.sub(r'^data:image/svg\+xml;base64,', '', b64, flags=re.I)
    svg_text = base64.b64decode(b64).decode('utf-8', 'replace')

    # фиксимо проблемні місця
    svg_text = _fix_opacity_percents(svg_text)
    svg_text = _fix_rem_to_px(svg_text, root_font_px=16.0)

    # рендер
    return cairosvg.svg2png(bytestring=svg_text.encode('utf-8'))
