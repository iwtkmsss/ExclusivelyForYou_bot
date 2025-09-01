import requests
from bs4 import BeautifulSoup
import json
import concurrent.futures
import os
import re
from bs4.element import NavigableString

# AD_PATTERNS = [
#     r'\binstagram\b', r'\btik[\-\s]?tok\b', r'\bfacebook\b', r'\byoutube\b',
#     r'\btelegram\b', r'телеграм', r'канал',
#     r'подпис', r'підпиш', r'follow', r'subscribe',
#     r'промокод', r'promo', r'знижк', r'скидк',
#     r'https?://', r'\B@[\w\.\-]+'  # @handle
# ]
# ad_regex = re.compile("|".join(AD_PATTERNS), re.IGNORECASE | re.UNICODE)
# def is_ad_text(text: str) -> bool:
#     return bool(ad_regex.search(text or ""))
#
#
# def run_in_parallel(func, args_list):
#     """
#     Запускає func у багатопроцесорному режимі, використовуючи всі ядра машини.
#
#     :param func: Функція, яку треба виконати
#     :param args_list: список аргументів (iterable), кожен елемент буде переданий у func
#     :return: список результатів
#     """
#     total = len(args_list) # optional
#     results = []
#     with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
#         futures = [executor.submit(func, arg) for arg in args_list]
#         for index, future in enumerate(concurrent.futures.as_completed(futures)):
#             results.append(future.result())
#             print(f"[{index}/{total}] готово") # optional
#     return results
#
#
# def scraping_url(url: str):
#     # ---- допоміжні "безпечні" геттери ----
#     def safe_text(node, default=None, sep=" ", strip=True):
#         try:
#             if node:
#                 return node.get_text(separator=sep, strip=strip)
#         except Exception as e:
#             pass
#         return default
#
#     def safe_attr(node, attr: str, default=None):
#         try:
#             if node and node.has_attr(attr):
#                 return node[attr]
#         except Exception:
#             pass
#         return default
#
#     # ---- мережа / soup ----
#     soup = None
#     try:
#         s = requests.Session()
#         resp = s.get(url, timeout=20)
#         resp.raise_for_status()
#         soup = BeautifulSoup(resp.text, "lxml")
#     except Exception:
#         # якщо сторінку не вдалося завантажити/розпарсити — повертаємо "скелет" із None
#         return {
#             "name": None,
#             "photo": None,
#             "ingredients": None,
#             "cooking_instructions": {"title": "Інструкція з приготування:\n\n", "steps": []},
#             "description": None,
#         }
#
#     # ---- фото (головне) ----
#     try:
#         photo = safe_attr(soup.select_one("div.tofu_image img"), "src")
#     except Exception:
#         photo = None
#
#     # ---- назва ----
#     try:
#         container = soup.select_one("div.max-lg\\:hidden.print\\:block h1")
#         name = safe_text(container) if container else None
#         if name:
#             name = name.strip()
#     except Exception:
#         name = None
#
#     # ---- інгредієнти ----
#     try:
#         ing_list = [li.get_text(" ", strip=True) for li in soup.select("div.ingredient-list ol li")]
#         ingredients = "Інгредієнти:\n\n" + "\n".join(ing_list) if ing_list else None
#     except Exception:
#         ingredients = None
#
#     # ---- опис без хештегів ----
#     try:
#         desc_p = soup.find(
#             "div",
#             class_="break-words text-cookpad-14 hidden lg:block print:block"
#         ).select_one("p")
#         # беремо тільки текстові вузли, ігноруючи <a>
#         contents = desc_p.contents if desc_p else []
#         description = "".join(node for node in contents if isinstance(node, NavigableString)).strip() or None
#     except Exception:
#         description = None
#
#     # ---- кроки інструкції: номер, текст, фото ----
#     steps = []
#     try:
#         li_nodes = soup.select("#steps ol li")
#         for idx, li in enumerate(li_nodes, start=1):
#             # номер
#             num = None
#             try:
#                 badge = li.select_one('[aria-label^="Крок"]')
#                 if badge and badge.has_attr("aria-label"):
#                     m = re.search(r'Крок\s*(\d+)', badge["aria-label"])
#                     if m:
#                         num = int(m.group(1))
#             except Exception:
#                 pass
#             if num is None:
#                 num = idx
#
#             # текст
#             try:
#                 p_tag = li.find("p")
#                 text = p_tag.get_text("\n", strip=True) if p_tag else safe_text(li, sep="\n")
#                 text = text or ""
#             except Exception:
#                 text = ""
#
#             # фільтр "рекламних" кроків
#             if (not text) or is_ad_text(text):
#                 continue
#
#             # фото для кроку
#             try:
#                 images = [img["src"] for img in li.find_all("img", src=True)]
#             except Exception:
#                 images = []
#
#             steps.append({"step": num, "text": text, "images": images})
#     except Exception:
#         # якщо розділ кроків поламаний, просто залишимо steps=[]
#         steps = []
#
#     cooking_instructions = {
#         "title": "Інструкція з приготування:\n\n",
#         "steps": steps
#     }
#
#     return {
#         "name": name,
#         "photo": photo,
#         "ingredients": ingredients,
#         "cooking_instructions": cooking_instructions,
#         "description": description
#     }
#
#
# def scrape_one(item):
#     key, url = item
#     try:
#         res = scraping_url(url)   # <- твой парсер
#     except Exception as e:
#         # не роняем весь процесс, просто вернём None
#         res = None
#     return key, res
#
#
# def main():
#     with open("recipes.json", "r", encoding="utf-8") as file:
#         recipes = json.load(file)
#
#     args_list = [(k, recipes[k]["link"]) for k in recipes.keys()]
#
#     pairs = run_in_parallel(scrape_one, args_list)
#
#     for key, result in pairs:
#         if result is not None:
#             recipes[key].update(result)
#         else:
#             recipes[key].setdefault("_error", True)
#
#     with open("recipess.json", "w+", encoding="utf-8") as file:
#         json.dump(recipes, file, indent=4, ensure_ascii=False)
#     # (scraping_url("https://cookpad.com/ua/recipes/24988036"))
#


def main():
    path = r"C:\my_fit_fit\ExclusivelyForYou_bot\ExclusivelyForYou_bot\misc\jokes_util\recipes.json"
    with open(path, "r", encoding="utf-8") as f:
        recipes = json.load(f)

    for i in recipes.keys():
        recipes[i].update({"used": False})

    with open(path, "w", encoding="utf-8") as f:
        json.dump(recipes, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
