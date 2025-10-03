from django.db import models
from slugify import slugify


class Slider(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    sort_order = models.IntegerField(default=0)
    url = models.CharField(default='#')
    image_desktop = models.ImageField(upload_to='slider_desktop_images')
    image_mobile = models.ImageField(upload_to='slider_mobile_images')

    class Meta:
        verbose_name = 'Slider'
        verbose_name_plural = "Sliders"
        ordering = ['sort_order']


    def save(self, *args, **kwargs):
        if not self.slug:
            # Генерируем слаг только если его нет
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Slider.objects.filter(slug=slug).exists():
                # если слаг уже существует — добавляем "-2", "-3" и т.д.
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


