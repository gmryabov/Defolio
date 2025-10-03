# from django.contrib import admin
# from . import models
#
#
# @admin.register(models.Shop)
# class ShopAdmin(admin.ModelAdmin):
#     model = models.Shop
#     list_display = ('id', 'title', 'is_active', 'updated_at')
#     list_display_links = ('id', 'title',)
#     prepopulated_fields = {"slug": ("title",)}
#
#
# @admin.register(models.Item)
# class ItemAdmin(admin.ModelAdmin):
#     model = models.Item
#     list_display = ('id', 'title', 'is_active', 'updated_at')
#     list_display_links = ('id', 'title',)
#     prepopulated_fields = {"slug": ("title",)}
#
#
# @admin.register(models.ItemCategory)
# class ItemTypeAdmin(admin.ModelAdmin):
#     model = models.ItemCategory
#     list_display = ('id', 'title', 'is_active')
#     list_display_links = ('id', 'title',)
#     prepopulated_fields = {"slug": ("title",)}
#
#
# @admin.register(models.ItemProperty)
# class ItemPropertyAdmin(admin.ModelAdmin):
#     model = models.ItemProperty
#     list_display = ('id', 'title', 'type')
#     list_display_links = ('id', 'title',)
#     prepopulated_fields = {"slug": ("title",)}
#
#
# @admin.register(models.ItemPropertyValue)
# class ItemPropertyValueAdmin(admin.ModelAdmin):
#     model = models.ItemPropertyValue
#     list_display = ('id', 'title', 'property')
#     list_display_links = ('id', 'title',)
#     prepopulated_fields = {"slug": ("title",)}
#
#
# @admin.register(models.ItemVariable)
# class ItemVariableAdmin(admin.ModelAdmin):
#     model = models.ItemVariable
#     list_display = ('id', 'item', 'property', 'property_value',)
#     list_display_links = ('id', 'item',)
#
#
# @admin.register(models.ItemVariablePrice)
# class ItemVariablePriceAdmin(admin.ModelAdmin):
#     model = models.ItemVariablePrice
#     list_display = ('id', 'variable', 'updated_at', 'value')
#     list_display_links = ('id', 'variable',)
#
#
# @admin.register(models.ItemVariableStock)
# class ItemVariableStockAdmin(admin.ModelAdmin):
#     model = models.ItemVariableStock
#     list_display = ('id', 'variable', 'updated_at', 'value')
#     list_display_links = ('id', 'variable',)
