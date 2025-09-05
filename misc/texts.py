class T:
    FOOD_RECIPE = """
Назва страви: <b>{name}</b>\n
{ingredients}\n
<i>{description}</i>
"""
    COCKTAIL_RECIPES = """
Назва коктейлю: <b>{name}</b>\n
{ingredients}\n
<i>{description}</i>
"""
    SWEETS_RECIPE = """
Назва солодкого: <b>{name}</b>\n
{ingredients}\n
<i>{description}</i>  
"""
    RECIPE_STEP = """
👩‍🍳 Крок {step}/{max_step} :\n
<i>{text}</i>
"""
    ZODIAC = """
<b>{title}</b>\n\n
<i>{text}</i>
"""
    MatrixOfDestinyPersonal = """
Знизу напиши будь-ласка ім'я та дату народження в форматі : \n   
----------------
Олег 01.04.2006
----------------
Ім'я дд.мм.рррр
----------------
Віка 10.08.2007
----------------\n
<i>Тоб-то просто через пробіл ім'я та дата народження, без ком і тд.</i> 
"""
    MatrixOfDestinyChoiceSex = """
<b>Обери стать для перевірки ⬇️</b> 
"""
    MATRIX_SPECIAL_QUALITIES = """
<b>{title}</b>\n
{intro_text}\n
<b>{positive_title}</b>\n
{positive_text}\n
<b>{negative_title}</b>\n
{negative_text}\n
<b>{communication_title}</b>\n
{communication_text}\n
"""