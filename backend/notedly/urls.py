from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='notedly'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<int:profile_id>', views.profile_view, name='profile'),
    path('post/<str:post_slug>', views.post_detail_view, name='post_detail'),
    path('ajax/toggle_relation/', views.toggle_relation, name='ajax_toggle_relation'),
    path('ajax/toggle-follow/', views.toggle_follow, name='ajax_toggle_follow'),
    path('ajax/updload_background/', views.upload_background, name='ajax_upload_background'),
    path('alax/post/comments/create/', views.create_comment, name='ajax_create_comment'),
    path('ajax/post/comments/edit/', views.edit_comment, name='ajax_edit_comment'),
    path('ajax/post/comments/delete/', views.delete_comment, name='ajax_delete_comment'),
    path('ajax/post/comments/like/', views.toggle_comment_like, name='ajax_like_comment'),
    path('ajax/post/toggle_publish/', views.toggle_post_publish, name='ajax_toggle_post_publish'),
    path('ajax/post/delete/', views.delete_post, name='ajax_delete_post'),
]
