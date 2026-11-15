from includes.computable_primitives import *
from includes.computable_legacy_primitives import *

def coffee_shop():
    shopping_cart = []
    visitShop()

def visitShop():
    terminal_display(message='Enter c to select coffee, anything else to exit.')
    user_choice = terminal_input()
    user_chose_coffee = equals(value1=user_choice, value2='c')
    if user_chose_coffee:
        terminal_display(message='User chose to add coffee to cart.')
        visitShop()
if __name__ == '__main__':
    coffee_shop()