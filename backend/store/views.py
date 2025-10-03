import os

from django.http import JsonResponse
from django.shortcuts import render, redirect
from . import models, forms


def get_shop(request):
    shop_id = request.GET.get("shop")
    if shop_id:
        return models.Shop.objects.get(id=shop_id)
    return models.Shop.objects.first()


def user_context(request):
    context = {
        'title': 'Панель управления магазином',
        'item_property_form': forms.ItemPropertyForm(),
        'item_property_value_form': forms.ItemPropertyValueForm(),
        'item_category_form': forms.CategoryForm(),
        'item_form': forms.ItemForm(),
        'shop_creation_form': forms.ShopForm(),
        'shops': models.Shop.objects.filter(is_active=True).all(),
        'shop': get_shop(request),
    }
    return context


def admin_home(request):
    return render(
        request,
        'store/admin/home/index.html',
        context=user_context(request)
    )


def admin_items(request):
    shop = get_shop(request)

    context = {
        'items': models.Item.objects.filter(shop=shop).all(),
    }

    return render(
        request,
        'store/admin/products/items/index.html',
        context=context | user_context(request)
    )


def _admin_get_main_image(item):
    prop = models.ItemProperty.objects.get(slug='osnovnoe-izobrazhenie')
    prop_assignment, _ = models.ItemPropertyAssignment.objects.get_or_create(
            item=item,
            property=prop,
        )
    if not _:
        return prop_assignment.image_value
    return None


def ajax_admin_update_item_pic(request):
    def del_image(p: models.ItemPropertyAssignment):
        if p.image_value and os.path.isfile(p.image_value.path):
            os.remove(p.image_value.path)

    item = models.Item.objects.get(pk=request.POST['item'])
    prop = models.ItemProperty.objects.get(slug='osnovnoe-izobrazhenie')
    prop_assignment, _ = models.ItemPropertyAssignment.objects.get_or_create(
            item=item,
            property=prop,
            defaults={'image_value': request.FILES['image_value']}
        )

    if not _:
        # Значит объект был, просто заменяем файл
        if prop_assignment.image_value:
            del_image(prop_assignment)

    # Сохраняем новое
    prop_assignment.image_value = request.FILES['image_value']
    prop_assignment.save()

    return JsonResponse({'success': True})



def admin_items_create(request):
    context = {
        'title': 'Создание товара'
    }
    if request.method == "POST":
        form = forms.ItemForm(request.POST)
        if form.is_valid():
            item = form.save()  # сохранили основной Item

            # обрабатываем нестандартные поля prop_x
            for key, value in request.POST.items():
                if key.startswith("prop_"):
                    prop_id = key.split("_", 1)[1]
                    try:
                        prop = models.ItemProperty.objects.get(id=prop_id)
                    except models.ItemProperty.DoesNotExist:
                        continue

                    # создаём связь
                    assignment = models.ItemPropertyAssignment.objects.create(
                        item=item,
                        property=prop,
                    )

                    # если у свойства type == "arr" → значение берём из ItemPropertyValue
                    if prop.type == "arr":
                        if value:
                            vals = models.ItemPropertyValue.objects.filter(id=value)
                            assignment.values.set(vals)

                    # если текст/число/булево → кладём в raw_value
                    else:
                        assignment.raw_value = value
                        assignment.save()
            return redirect('admin_item', item_id=item.id)
        else:
            return JsonResponse(form.errors, status=400)

    return render(
        request,
        'store/admin/products/items/include/item_creation.html',
        context=context | user_context(request)
    )

def ajax_admin_get_category_props(request):
    category_id = request.POST.get('category_id')
    category = models.ItemCategory.objects.get(id=category_id)
    return JsonResponse(
        {
            'category': {
                'id': category.id,
                'title': category.title,
            },
            'props': [
                {
                    'id': p.id,
                    'title': p.title,
                    'slug': p.slug,
                    'type': p.type,
                    'values': [{v.id: v.title for v in p.values.all()}],
                }
                for p in category.properties.all()
            ]
        }
    )



def admin_item_detail(request, item_id):
    item = models.Item.objects.get(id=item_id)
    context = {
        'item': item,
        'main_image': _admin_get_main_image(item),
    }
    return render(
        request,
        'store/admin/products/detail/index.html',
        context=context | user_context(request)
    )


def admin_items_categories(request):
    shop = get_shop(request)

    context = {
        'categories': models.ItemCategory.objects.filter(shop=shop).all(),
    }

    if request.method == "POST":
        try:
            form = forms.CategoryForm(request.POST)
            if form.is_valid():
                form.save()


        except Exception as e:
            return JsonResponse({'error': str(e)})


    return render(
        request,
        'store/admin/products/categories/index.html',
        context=context | user_context(request)
    )


def admin_items_properties(request):
    shop = get_shop(request)

    context = {
        'properties': models.ItemProperty.objects.filter(shop=shop).order_by('title'),
    }
    if request.method == "POST":
        try:
            # Создаём свойство
            item_property = models.ItemProperty.objects.create(
                title=request.POST.get("title"),
                description=request.POST.get("description"),
                is_active=request.POST.get("is_active") == "on",
                is_aspect=request.POST.get("is_aspect") == "on",
                is_required=request.POST.get("is_required") == "on",
                is_multiply=request.POST.get("is_multiply") == "on",
                type=request.POST.get("type"),
                shop=shop,
            )

            prop_values = request.POST.getlist("prop_value[]")
            is_active_flags = request.POST.getlist("is_active[]")

            # Создаём значения свойства
            for i, value in enumerate(prop_values):
                if not value.strip():
                    continue  # пропускаем пустые

                flag = str(i + 1) in is_active_flags  # активность по индексу/значению
                models.ItemPropertyValue.objects.create(
                    title=value.strip(),
                    property=item_property,
                    is_active=flag
                )

            return redirect('admin_items_properties')

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return render(
        request,
        'store/admin/products/properties/index.html',
        context=context | user_context(request)
    )


# def ajax_admin_items_properties(request):
#     if request.method == "POST":
#         try:
#             # Получаем данные формы
#             title = request.POST.get("title")
#             description = request.POST.get("description")
#             category_id = request.POST.get("category")
#             is_active = request.POST.get("is_active") == "on"
#             is_aspect = request.POST.get("is_aspect") == "on"
#             is_required = request.POST.get("is_required") == "on"
#
#             prop_values = request.POST.getlist("prop_value[]")
#             is_active_flags = request.POST.getlist("is_active[]")
#
#             # Создаём свойство
#             category = models.ItemCategory.objects.get(pk=category_id)
#             item_property = models.ItemProperty.objects.create(
#                 title=title,
#                 description=description,
#                 category=category,
#                 is_active=is_active,
#                 is_aspect=is_aspect,
#                 is_required=is_required,
#             )
#
#             # Создаём значения свойства
#             for i, value in enumerate(prop_values):
#                 if not value.strip():
#                     continue  # пропускаем пустые
#
#                 flag = str(i+1) in is_active_flags  # активность по индексу/значению
#                 models.ItemPropertyValue.objects.create(
#                     title=value.strip(),
#                     property=item_property,
#                     is_active=flag
#                 )
#
#             return JsonResponse({"success": True, "id": item_property.id})
#
#         except Exception as e:
#             return JsonResponse({"success": False, "error": str(e)})
#
    # return JsonResponse({"success": False, "error": "Метод не поддерживается"})


def admin_warehouses(request):
    shop = get_shop(request)
    context = {
        'warehouses': models.Warehouse.objects.filter(shop=shop).all(),
    }
    return render(request, 'store/admin/warehouses/index.html', context=context | user_context(request))


def admin_shops(request):
    context = {
        'shops': models.Shop.objects.all(),
    }

    if request.method == "POST":
        form = forms.ShopForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_shops')
        else:
            return JsonResponse({"success": False, 'error': form.errors})

    return render(request, 'store/admin/shops/index.html', context=context | user_context(request))


def admin_shop_detail(request, shop_id):
    shop = models.Shop.objects.get(id=shop_id)
    context = {
        'shop_detail': shop
    }

    if request.method == "POST":
        form = forms.ShopForm(request.POST, instance=shop)
        if form.is_valid():
            form.save()
            return redirect('admin_shop_detail', shop_id=shop_id)
    return render(request, 'store/admin/shops/detail/index.html', context=context | user_context(request))


def ajax_admin_shop_logo_image(request):
    def del_image(s: models.Shop):
        if s.logo and os.path.isfile(s.logo.path):
            os.remove(s.logo.path)

    shop = models.Shop.objects.get(id=request.POST['shop_id'])
    del_image(shop)
    shop.logo = request.FILES['logo']
    shop.save()
    return JsonResponse({'success': True})


def ajax_admin_save_shop(request):
    title = request.POST.get('title')
    description = request.POST.get('description')
    is_active = request.POST.get('is_active') == 'true'
    shop_id = request.POST.get('shop_id')

    shop = models.Shop.objects.get(id=shop_id)
    shop.title = title
    shop.description = description
    shop.is_active = is_active
    shop.save()
    return JsonResponse({
        'success': True,
        'shop_id': shop_id,
        'title': title,
        'description': description,
        'is_active': is_active,
    })