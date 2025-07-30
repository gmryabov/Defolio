import json
import os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import localtime
from django.views.decorators.http import require_POST
from . import models
from .forms import LoginForm, UserRegisterForm, PostCreateForm
from .models import Post


# Главная
def home(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'login':
            login_form = LoginForm(request, data=request.POST)
            if login_form.is_valid():
                login_name = request.POST.get('username')
                password = request.POST.get('password')

                # Попробуем аутентифицировать пользователя по имени пользователя
                user = authenticate(request, username=login_name, password=password)

                # Если пользователь не найден, проверим по email
                if user is None:
                    try:
                        # Найдем пользователя по email
                        user = User.objects.get(email=login_name)
                        # Проверим пароль
                        if user.check_password(password):
                            user = user  # Установим найденного пользователя
                    except User.DoesNotExist:
                        user = None  # Если пользователь не найден по email

                # Если пользователь найден, выполняем вход
                if user is not None and user.is_active:
                    login(request, user)
                    return redirect('notedly')
            else:
                return JsonResponse({"error": login_form.errors, "data": request.POST}, status=400)
        elif action == 'register':
            register_form = UserRegisterForm(request.POST)
            if register_form.is_valid():
                user = register_form.save(commit=False)
                user.first_name = register_form.cleaned_data['first_name']
                user.last_name = register_form.cleaned_data['last_name']
                user.save()

                # Создаём профиль
                profile_pic = register_form.cleaned_data.get('profile_pic')
                models.Profile.objects.create(user=user, profile_pic=profile_pic)

                login(request, user)  # авторизуем после регистрации
                return redirect('notedly')
            else:
                return JsonResponse({"error": register_form.errors, "data": request.POST}, status=400)
        elif action == 'new_post':
            _new_post(request)
            return redirect('notedly')

    if 'category' in request.GET:
        posts = models.Post.objects.filter(
            categories__slug=request.GET['category'],
            is_published=True,
            is_deleted=False).order_by('-created_at')
    else:
        posts = models.Post.objects.order_by('-created_at')
    context = {
        'title': 'Главная',
        'login_form': LoginForm(),
        'register_form': UserRegisterForm(),
        'posts': posts,
    }
    return render(request, 'notedly/home/index.html', context=context | _get_context(request))

# Для сохранения правила DRY
def _get_context(request):
    context ={
        'categories': models.Category.objects.all(),
        'empty_topic': models.Category.objects.filter(title='Без темы').first(),
        'post_form': PostCreateForm(),
        'users': models.Profile.objects.annotate(followers_count=Count('followers')).order_by('-followers_count')[:3],
        'top_comments': models.Comment.objects.annotate(likes_count=Count('likes')).order_by('-likes_count')[:10],
    }
    return context

# Для сохранения правила DRY
def _new_post(request):
    post_id = request.POST.get('post_id')
    category_id = request.POST.get('category')

    post = None
    if post_id:
        post = get_object_or_404(Post, id=post_id, author=request.user.profile)
    post_form = PostCreateForm(request.POST, instance=post)

    if post_form.is_valid():
        post = post_form.save(commit=False)
        post.author = request.user.profile
        post.is_published = True
        post.save()
        post_form.save_m2m()
        try:
            category = models.Category.objects.get(id=int(category_id))
            post.categories.clear()
            post.categories.add(category)
        except models.Category.DoesNotExist:
            pass

# выход
def logout_view(request):
    logout(request)
    return redirect('notedly')

# Лайки и закладки у постов
@require_POST
@login_required
def toggle_relation(request):
    post_id = request.POST.get('post_id')
    action = request.POST.get('action')  # 'like' или 'bookmark'
    profile = request.user.profile

    if action not in ['like', 'bookmark']:
        return HttpResponseBadRequest("Invalid action.")

    post_model = models.Post
    try:
        post = post_model.objects.get(id=post_id)
    except post_model.DoesNotExist:
        return JsonResponse({'error': 'Post not found.'}, status=404)

    related_manager = getattr(post, f'{action}s', None)
    if related_manager is None:
        return HttpResponseBadRequest("Invalid relation.")

    field_name = f'{action}ed'

    if profile in related_manager.all():
        related_manager.remove(profile)
        toggled = False
    else:
        related_manager.add(profile)
        toggled = True

    return JsonResponse({
        field_name: toggled,
        f'{action}s_count': related_manager.count()
    })


# Подписка
@require_POST
@login_required
def toggle_follow(request):
    target_id = request.POST.get('target_id')
    current_user_profile = request.user.profile
    target_profile = models.Profile.objects.get(id=target_id)

    if target_profile in current_user_profile.following.all():
        current_user_profile.following.remove(target_profile)
        following = False
    else:
        current_user_profile.following.add(target_profile)
        following = True

    return JsonResponse({
        'following': following,
        'followers_count': target_profile.followers.count()
    })


@login_required
@require_POST
def upload_background(request):
    def del_image(p):
        # Удаляем старое изображение, если оно есть
            old_path = p.background.path
            if os.path.isfile(old_path):
                os.remove(old_path)

    profile = request.user.profile
    image = request.FILES.get('background')
    action = request.POST.get('action')

    if action == 'upload':
        if not image:
            return JsonResponse({'success': False, 'error': 'Нет файла'})

        # Удаляем старое изображение, если оно есть
        if profile.background and profile.background.name:
            del_image(profile)

        profile.background = image
        profile.save()

        return JsonResponse({
            'success': True,
            'image_url': profile.background.url
        })
    elif action == 'delete':
        if profile.background and profile.background.name:
            del_image(profile)
            profile.background = None
            profile.save()

        return JsonResponse({
            'success': True,
        })
    return JsonResponse({
            'success': False,
        })


# профиль
def profile_view(request, profile_id):
    profile = models.Profile.objects.get(id=profile_id)
    context = {
        'profile': profile,
        'title': f"{profile.user.first_name} (@{profile.user.username})",
        'comments': models.Comment.objects.filter(author=profile).order_by('-created_at'),
    }

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'new_post':
            _new_post(request)
            return redirect('profile')

    return render(request, 'notedly/profile/index.html', context=context | _get_context(request))


# пост детально
def post_detail_view(request, post_slug):
    post = Post.objects.get(slug=post_slug)
    context = {
        'post': post,
        'title': post.title,
    }
    return render(request, 'notedly/post/detail/index.html', context=context | _get_context(request))


@require_POST
@login_required
def create_comment(request):
    content = request.POST.get('content')
    post_id = request.POST.get('post_id')
    parent_id = request.POST.get('parent_id')

    if not content or not post_id:
        return JsonResponse({'success': False, 'error': 'Missing fields'})

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Post not found'})

    parent = models.Comment.objects.filter(id=parent_id).first() if parent_id else None

    comment = models.Comment.objects.create(
        post=post,
        author=request.user.profile,
        content=content,
        parent=parent
    )

    return JsonResponse({
        'success': True,
        'comment_id': comment.id,
        'content': comment.content,
        'username': comment.author.user.username,
        'profile_pic_url': comment.author.profile_pic.url if comment.author.profile_pic else None,
        'created_at': localtime(comment.created_at).strftime('%d.%m.%Y %H:%M')
    })


@require_POST
@login_required
def edit_comment(request):
    try:
        data = json.loads(request.body)
        comment_id = data.get("id")
        content = data.get("content", "").strip()

        if not content:
            return JsonResponse({"error": "Пустой комментарий"}, status=400)

        comment = get_object_or_404(models.Comment, id=comment_id)
        if comment.content == content:
            return JsonResponse({"error": "Комментарий не изменился"}, status=400)

        comment.content = content
        comment.is_edited = True
        comment.save()

        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@require_POST
@login_required
def delete_comment(request):
    try:
        data = json.loads(request.body)
        comment_id = data.get("id")
        comment = get_object_or_404(models.Comment, id=comment_id)

        comment.is_deleted = True
        comment.save()

        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# Лайки комментариев
@require_POST
@login_required
def toggle_comment_like(request):
    comment_id = request.POST.get('comment_id')
    profile = request.user.profile
    try:
        comment = models.Comment.objects.get(id=comment_id)
    except models.Comment.DoesNotExist:
        return JsonResponse({'error': 'Post not found.'}, status=404)

    if profile in comment.likes.all():
        comment.likes.remove(profile)
        toggled = False
    else:
        comment.likes.add(profile)
        toggled = True

    return JsonResponse({
        'liked': toggled,
        f'likes_count': comment.likes.count()
    })


@require_POST
@login_required
def toggle_post_publish(request):
    data = json.loads(request.body)
    post_id = data.get('post_id')
    post = get_object_or_404(Post, id=post_id, author=request.user.profile)
    post.is_published = not post.is_published
    post.save()
    return JsonResponse({'success': True, 'is_published': post.is_published})


@require_POST
@login_required
def delete_post(request):
    data = json.loads(request.body)
    post_id = data.get('post_id')
    post = get_object_or_404(Post, id=post_id, author=request.user.profile)
    post.is_deleted = True
    post.save()
    return JsonResponse({'success': True, 'deleted': post.is_deleted})
