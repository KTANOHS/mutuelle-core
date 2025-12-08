from django import template

register = template.Library()

@register.simple_tag
def query_string_remove(param_name):
    """
    Retourne l'URL actuelle sans le paramètre spécifié
    Utilisation: {% query_string_remove 'param_name' %}
    """
    from django.http import QueryDict
    from urllib.parse import urlencode
    
    request = template.resolve_request()
    query_dict = request.GET.copy()
    
    if param_name in query_dict:
        del query_dict[param_name]
    
    return urlencode(query_dict)