from django import template

from store import models


register = template.Library()

@register.filter
def prop_assignment(assignments, prop):
    return assignments.filter(property=prop).first()

#
@register.filter
def get_image(item):
    prop = models.ItemProperty.objects.get(slug='osnovnoe-izobrazhenie')
    assign, _ = models.ItemPropertyAssignment.objects.get_or_create(
            item=item,
            property=prop,
        )
    if not _:
        return assign.image_value.url
    return None