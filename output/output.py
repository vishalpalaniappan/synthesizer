from includes.computable_primitives import *
from includes.computable_legacy_primitives import *

def coffee_shop():
    shopping_cart = []
    visitShop()

def visitShop():
    terminal_display()
    user_choice = terminal_input()
    user_chose_coffee = equals(value1='user_choice', value2='coffee')
    if user_chose_coffee:
        terminal_display()
        visitShop()