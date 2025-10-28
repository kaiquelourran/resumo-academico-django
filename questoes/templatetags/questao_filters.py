from django import template

register = template.Library()

@register.filter
def index(value, arg):
    """
    Retorna o caractere no índice especificado
    Uso: {{ "ABCDE"|index:0 }} → "A"
    """
    if isinstance(value, str) and isinstance(arg, int) and 0 <= arg < len(value):
        return value[arg]
    return ''

