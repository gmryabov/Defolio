from django.urls import path
from . import views
#
urlpatterns = [
    path('admin/', views.admin_home, name='admin_home'),
    path('admin/items/list/', views.admin_items, name='admin_items'),
    path('admin/items/list/<int:item_id>/', views.admin_item_detail, name='admin_item'),
    path('admin/items/list/create/', views.admin_items_create, name='admin_items_create'),
    path('admin/items/categories/', views.admin_items_categories, name='admin_items_categories'),

    path('admin/items/properties/', views.admin_items_properties, name='admin_items_properties'),
    # path('ajax/admin/items/properties/', views.ajax_admin_items_properties, name='ajax_admin_items_properties'),

    path('admin/warehouses/', views.admin_warehouses, name='admin_warehouses'),
    path('admin/shops/', views.admin_shops, name='admin_shops'),
    path('admin/shops/<int:shop_id>/', views.admin_shop_detail, name='admin_shop_detail'),
    path(
        'ajax/admin/get/category/props/',
         views.ajax_admin_get_category_props,
         name='ajax_admin_get_category_props'
    ),
    path('ajax/admin/update/item/pic/', views.ajax_admin_update_item_pic, name='ajax_admin_update_item_pic'),
    path('ajax/admin/shop/logo/image/', views.ajax_admin_shop_logo_image, name='ajax_admin_shop_logo_image'),
    path('ajax/admin/shop/save/', views.ajax_admin_save_shop, name='ajax_admin_save_shop'),
]