from django import template

register = template.Library()

@register.filter
def format_with_suffix(value):
    value = int(value)
    if value % 10 == 1 and value % 100 != 11:
        suffix = 'лайк'
    elif 2 <= value % 10 <= 4 and not (12 <= value % 100 <= 14):
        suffix = 'лайка'
    else:
        suffix = 'лайков'
    return f"{value} {suffix}"


@register.filter
def follower_with_suffix(value):
    value = int(value)
    if value % 10 == 1 and value % 100 != 11:
        suffix = 'подписчик'
    elif 2 <= value % 10 <= 4 and not (12 <= value % 100 <= 14):
        suffix = 'подписчика'
    else:
        suffix = 'подписчиков'
    return f"{value} {suffix}"


@register.filter
def following_with_suffix(value):
    value = int(value)
    if value % 10 == 1 and value % 100 != 11:
        suffix = 'подписка'
    elif 2 <= value % 10 <= 4 and not (12 <= value % 100 <= 14):
        suffix = 'подписки'
    else:
        suffix = 'подписок'
    return f"{value} {suffix}"