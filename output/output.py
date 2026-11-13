from includes.computable_primitives import *
from includes.computable_legacy_primitives import *

def coffee_shop():
    shopping_cart = []
    visitShop()

def visitShop():
    terminal_display()
    terminal_input()
    user_chose_coffee = checkIfUserChoseCoffee()
    if user_chose_coffee:
        terminal_display()
        visitShop()

def checkIfUserChoseCoffee():
    equals()