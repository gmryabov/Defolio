from django.contrib import admin

from .models import Slider


# Register your models here.
@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    fields = ['is_active', 'title', 'subtitle', 'sort_order', 'url', 'image_mobile', 'image_desktop']
    search_fields = ['title']
    sortable_field_name = 'sort_order'
    list_display = ('title', 'is_active', 'created_at', 'updated_at')