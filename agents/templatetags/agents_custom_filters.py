from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    '''Multiplie la valeur par l'argument'''
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def divisibleby(value, arg):
    '''Vérifie si la valeur est divisible par l'argument'''
    try:
        return int(value) % int(arg) == 0
    except (ValueError, TypeError):
        return False

@register.filter
def get_item(dictionary, key):
    '''Récupère un élément d'un dictionnaire'''
    return dictionary.get(key)

@register.filter
def add(value, arg):
    '''Additionne la valeur et l'argument'''
    try:
        return int(value) + int(arg)
    except (ValueError, TypeError):
        try:
            return str(value) + str(arg)
        except:
            return value
