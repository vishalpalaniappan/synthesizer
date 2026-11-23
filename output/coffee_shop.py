from includes.computable_primitives import *
from includes.computable_legacy_primitives import *

def coffee_shop():
    global shopping_cart
    shopping_cart = []
    terminal_display(message='\nWelcome to Cabbage Corp Coffee Shop.')
    visitShop()
    terminal_display(message='Thanks for visiting cabbage corp coffee shop.')

def visitShop():
    menu = '\nEnter a to add coffee to cart($1.80), d to display shopping cart, c to checkout and anything else to exit.'
    terminal_display(message=menu)
    user_choice = terminal_input()
    user_chose_coffee = equals(value1=user_choice, value2='a')
    if user_chose_coffee:
        addCoffeeToCart()
        visitShop()
    user_chose_display = equals(value1=user_choice, value2='d')
    if user_chose_display:
        displayCart()
        visitShop()
    user_chose_checkout = equals(value1=user_choice, value2='c')
    if user_chose_checkout:
        checkoutCart()

def addCoffeeToCart():
    terminal_display(message='User chose to add coffee to cart.')
    insert_at_end_of_list(item='coffee', list=shopping_cart)

def displayCart():
    terminal_display(message='User chose to display cart.')
    terminal_display(message=shopping_cart)

def checkoutCart():
    terminal_display(message='User chose to checkout cart.')
    numItemsInCart = get_length(list=shopping_cart)
    coffee_cost = 1.8
    global total_cart_cost
    total_cart_cost = None
    total_cart_cost = multiply(multiplicand=numItemsInCart, multiplier=coffee_cost)
    acceptPayment()

def acceptPayment():
    terminal_display(message='\nPlease enter the amount owed to pay bill (in CAD):')
    terminal_display(message=total_cart_cost)
    user_payment = terminal_input()
    user_payment_num = cast_string_to_float(str=user_payment)
    payment_invalid = not_equals(value1=user_payment_num, value2=total_cart_cost)
    if payment_invalid:
        terminal_display(message='Payment invalid, try again.')
        acceptPayment()
if __name__ == '__main__':
    coffee_shop()