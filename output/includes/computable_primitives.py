def insert_at_end_of_list(item, list):
    list.append(item)
    return list

def remove_from_end_of_list(list):
    list.pop()
    return list

def clear_list(list):
    list = []
    return list

def equals(value1, value2):
    return value1 == value2

def not_equals(value1, value2):
    return value1 != value2

def multiply(multiplicand, multiplier):
    return multiplicand * multiplier

def get_length(list):
    return len(list)

def cast_string_to_float(str):
    return float(str)