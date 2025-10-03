from django.db import models
from slugify import slugify


class Shop(models.Model):
    is_active = models.BooleanField(verbose_name="Активность", default=True)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)
    title = models.CharField("Наименование", max_length=255)
    slug = models.SlugField(verbose_name="Символьный код", max_length=255, unique=True)
    description = models.TextField(verbose_name="Описание магазина", blank=True)
    logo = models.ImageField(verbose_name="Лого", upload_to="logo", blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Генерируем слаг только если его нет
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Shop.objects.filter(slug=slug).exists():
                # если слаг уже существует — добавляем "-2", "-3" и т.д.
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Магазины"
        verbose_name = "Магазин"
        ordering = ['-created_at']


class Warehouse(models.Model):
    is_active = models.BooleanField(verbose_name="Активность", default=True)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)
    title = models.CharField("Наименование", max_length=255)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='warehouses')
    slug = models.SlugField(verbose_name="Символьный код", max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Генерируем слаг только если его нет
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Warehouse.objects.filter(slug=slug).exists():
                # если слаг уже существует — добавляем "-2", "-3" и т.д.
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Склады"
        verbose_name = "Склад"
        ordering = ['-created_at']


class Item(models.Model):
    is_active = models.BooleanField(verbose_name="Активность", default=True)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)
    title = models.CharField("Наименование", max_length=255)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='items')
    category = models.ForeignKey(
        'ItemCategory',
        verbose_name="Тип товара",
        on_delete=models.CASCADE,
        related_name='items',
        blank=True,
        null=True
    )
    slug = models.SlugField(verbose_name="Символьный код", max_length=255, unique=True)
    sku = models.CharField(verbose_name="Артикул", max_length=255, unique=True)
    uuid = models.UUIDField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Генерируем слаг только если его нет
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Item.objects.filter(slug=slug).exists():
                # если слаг уже существует — добавляем "-2", "-3" и т.д.
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Товары"
        verbose_name = "Товар"


class ItemCategory(models.Model):
    is_active = models.BooleanField(verbose_name="Активность", default=True)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)
    title = models.CharField("Наименование", max_length=255)
    slug = models.SlugField(verbose_name="Символьный код", max_length=255, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    properties = models.ManyToManyField('ItemProperty', related_name='properties', blank=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='categories', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Генерируем слаг только если его нет
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while ItemCategory.objects.filter(slug=slug).exists():
                # если слаг уже существует — добавляем "-2", "-3" и т.д.
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Категории"
        verbose_name = "Категория"
        ordering = ['-created_at']



class PropertyType(models.TextChoices):
    ARRAY = 'arr', 'Список'
    BOOLEAN = 'bool', 'Флаг'
    TEXT = 'text', 'Строка'
    NUMBER = 'number', 'Число'
    FILE = 'file', 'Файл'
    IMAGE = 'img', 'Изображение'


class ItemProperty(models.Model):
    is_active = models.BooleanField(verbose_name="Активность", default=True)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)
    title = models.CharField("Наименование", max_length=255)
    # category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, related_name='properties', verbose_name="Тип товара")
    slug = models.SlugField(verbose_name="Символьный код", max_length=255, unique=True)
    is_aspect = models.BooleanField(verbose_name="Аспектное свойство", default=False)
    is_required = models.BooleanField(verbose_name="Обязательный", default=False)
    is_multiply = models.BooleanField(verbose_name="Множественное значение1", default=False)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    type = models.CharField(
        'Тип свойства',
        max_length=50,
        null=True,
        blank=True,
        choices=PropertyType.choices
    )
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='properties', blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            # Генерируем слаг только если его нет
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while ItemProperty.objects.filter(slug=slug).exists():
                # если слаг уже существует — добавляем "-2", "-3" и т.д.
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Свойства товаров"
        verbose_name = "Свойство товара"
        ordering = ['-created_at']



class ItemPropertyValue(models.Model):
    is_active = models.BooleanField(verbose_name="Активность", default=True)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)
    title = models.CharField("Наименование", max_length=255, unique=True)

    property = models.ForeignKey(
        ItemProperty,
        on_delete=models.CASCADE,
        related_name='values',
        verbose_name="Свойство"
    )
    slug = models.SlugField(verbose_name="Символьный код", max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Генерируем слаг только если его нет
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while ItemPropertyValue.objects.filter(slug=slug).exists():
                # если слаг уже существует — добавляем "-2", "-3" и т.д.
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Значения свойств"
        verbose_name = "Значение свойства"
        ordering = ['title']


class ItemPropertyAssignment(models.Model):
    """Связь товара и свойства с выбранным значением."""
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='prop_assignments')
    property = models.ForeignKey(ItemProperty, on_delete=models.CASCADE, related_name="assignments")
    # если type != arr → сюда кладём текст/число/булево
    raw_value = models.CharField("Значение", max_length=255, blank=True, null=True)
    image_value = models.ImageField("Изображение", upload_to="items", blank=True, null=True)
    # если type == arr → выбираем из справочника
    values = models.ManyToManyField(ItemPropertyValue, blank=True, related_name="assignments")
    def __str__(self):
        return f"{self.property}"


class ItemVariable(models.Model):
    is_active = models.BooleanField(verbose_name="Активность", default=True)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='variables',
        verbose_name="Товар"
    )
    property = models.ForeignKey(
        ItemProperty,
        on_delete=models.CASCADE,
        related_name='variables',
        verbose_name="Свойство"
    )
    property_value = models.ForeignKey(
        ItemPropertyValue,
        verbose_name="Значение",
        on_delete=models.CASCADE,
        related_name='variables'
    )
    slug = models.SlugField(verbose_name="Символьный код", max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Генерируем слаг только если его нет
            base_slug = slugify(f"{self.item.title} - {self.property.title} {self.property_value.title}")
            slug = base_slug
            counter = 1
            while ItemVariable.objects.filter(slug=slug).exists():
                # если слаг уже существует — добавляем "-2", "-3" и т.д.
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item.title} - {self.property.title} - {self.property_value.title}"

    class Meta:
        unique_together = ('item', 'property', 'property_value')
        verbose_name_plural = 'Варианты товара'
        verbose_name = 'Вариант товара'


class ItemPrice(models.Model):
    is_active = models.BooleanField(verbose_name="Активность", default=True)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)
    value = models.DecimalField(verbose_name="Значение", decimal_places=2, max_digits=10)
    item = models.ForeignKey(
        Item,
        verbose_name='Вариант товара',
        on_delete=models.CASCADE,
        related_name='prices'
    )

    def __str__(self):
        return f"{self.value}"

    class Meta:
        unique_together = ('value', 'item')
        verbose_name_plural = 'Цены товаров'
        verbose_name = 'Цена товара'


class ItemStock(models.Model):
    is_active = models.BooleanField(verbose_name="Активность", default=True)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)
    value = models.PositiveIntegerField(verbose_name="Значение", default=0)
    item = models.ForeignKey(
        Item,
        verbose_name='Вариант товара',
        on_delete=models.CASCADE,
        related_name='stocks'
    )

    def __str__(self):
        return f"{self.value}"

    class Meta:
        unique_together = ('value', 'item')
        verbose_name_plural = "Остатки товаров"
        verbose_name = "Остаток товара"
