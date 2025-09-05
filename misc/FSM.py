from aiogram.fsm.state import StatesGroup, State


class Paginations(StatesGroup):
    FoodRecipes = State()
    CocktailRecipes = State()
    SweetsRecipe = State()
    PaginationPersonalMatrix = State()

class MatrixOfDestiny(StatesGroup):
    Personal = State()
    Compatibility = State()
