from aiogram.fsm.state import StatesGroup, State


class Paginations(StatesGroup):
    FoodRecipes = State()
    CocktailRecipes = State()
    SweetsRecipe = State()
