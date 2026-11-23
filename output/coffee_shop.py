from includes.computable_primitives import *
from includes.computable_legacy_primitives import *

def coffee_shop():
    global shopping_cart
    shopping_cart = []
    visitShop()
    terminal_display(message='Goodbye')

def visitShop():
    menu = 'Enter c to select coffee, d to display shopping cart, anything else to exit.'
    terminal_display(message=menu)
    user_choice = terminal_input()
    user_chose_coffee = equals(value1=user_choice, value2='c')
    if user_chose_coffee:
        addCoffeeToCart()
        visitShop()
        visitShop()
    user_chose_display = equals(value1=user_choice, value2='d')
    if user_chose_display:
        displayCart()
        visitShop()
        visitShop()

def addCoffeeToCart():
    terminal_display(message='User chose to add coffee to cart.')
    insert_at_end_of_list(item='coffee', list=shopping_cart)

def displayCart():
    terminal_display(message='User chose to display cart.')
    terminal_display(message=shopping_cart)
if __name__ == '__main__':
    coffee_shop()