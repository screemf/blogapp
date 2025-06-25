from django import template

register = template.Library()

'''Для дерева коментариев отступ в 20 пикселей '''
@register.filter
def get_comment_indent(level):
    return level * 20