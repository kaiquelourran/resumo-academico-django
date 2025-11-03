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

@register.filter
def iniciais(nome):
    """
    Retorna as iniciais de um nome.
    Ex: "João Silva" -> "JS"
    Ex: "Maria" -> "MM"
    """
    if not nome:
        return "??"
    
    partes = nome.strip().split()
    if len(partes) >= 2:
        # Pega primeira letra do primeiro nome e primeira letra do último nome
        return (partes[0][0] + partes[-1][0]).upper()
    elif len(partes) == 1:
        # Se só tem um nome, usa a primeira letra duas vezes
        primeira_letra = partes[0][0].upper()
        return primeira_letra + primeira_letra
    return "??"
