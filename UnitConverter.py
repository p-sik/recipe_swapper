# TODO multiple units on same line?
# TODO error handling
# FIXME the mess you've made

from typing import List
import math


def extract_conversion(path: str) -> dict:
    """
    read pairs of units for conversion from given file
    return a dict with key_values pairs   
    """ 
    values_table = dict()
    source_file = open(path)

    conv_list = source_file.readlines()
    # pop header if present
    if conv_list[0].startswith("#"):
        conv_list.pop(0)

    for item in conv_list:
        item = item.rstrip()
        sep_list = item.split()
        key = sep_list[0]
        value = float(sep_list[1])
        values_table[key] = value
    
    return values_table

def parse_recipe(recipe: List[str]) -> List[str]:
    """
    parse each line of the recipe and replace cups with grams
    match: number + optional ("of") + item
    """
    new_recipe: List[str] = list()
    for line in recipe:
        unit: bool = False
        quantity: bool = False
        unit_index: int = 0
        unit_length: int = 0
        quantity_index: int = 0
        quantity_length: int = 0

        line = line.lstrip().rstrip()
        words = line.split()
        for word in words:
            if word in VOLUMES.keys():
                if unit is False:
                    unit_index = line.index(word)
                    unit_length = len(word)
                    unit = True
            
            if word in DENSITIES.keys():
                quantity_index = line.index(word)
                quantity_length = len(word)
                quantity = True

        if quantity and unit:
            number = convert_to_float(line[0:unit_index])
            qty = line[quantity_index:quantity_index + quantity_length]
            unt = line[unit_index:unit_index + unit_length]
            
            print('Swapping candidate: \"{:}\"'.format(line))
            new_number = number * VOLUMES[unt] * DENSITIES[qty]
            new_number = math.ceil(new_number)
            new_line = line.replace(line[0:unit_index],  '{:.2f} '.format(new_number))
            new_line = new_line.replace(unt, "g")
            print('Swapped to: \"{:}\"'.format(new_line))
            print(40 * "-")
            new_recipe.append(new_line)

    return new_recipe


def convert_to_float(input: str) -> float:
    try:
        return float(input)
    except ValueError:
        num, denom = input.split('/')
        try:
            leading, num = num.split(' ')
            whole = float(leading)
        except ValueError:
            whole = 0
        frac = float(num) / float(denom)
        return whole - frac if whole < 0 else whole + frac


RECIPE = open("sample_recipe.txt").readlines()

DENSITIES = extract_conversion("densities.txt")
VOLUMES = extract_conversion("units.txt")

new_rec = parse_recipe(RECIPE)
print(new_rec)
if len(new_rec) != len(RECIPE):
    print("\nNot all parsed")
