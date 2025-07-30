from django.contrib import admin

from .models import Category, Profile


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile

