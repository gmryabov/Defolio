from django.contrib.auth.models import User
from django.db import models
from slugify import slugify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    background = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    likes = models.ManyToManyField(Profile, blank=True, related_name='liked_posts')
    bookmarks = models.ManyToManyField(Profile, blank=True, related_name='bookmarks')
    title = models.CharField(max_length=100)
    content = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            # Генерируем слаг только если его нет
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                # если слаг уже существует — добавляем "-2", "-3" и т.д.
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    likes = models.ManyToManyField(Profile, blank=True, related_name='liked_comments')

    def __str__(self):
        return f"Comment by {self.author.user.username} on {self.post.title}"



class Category(models.Model):
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    posts = models.ManyToManyField(Post, blank=True, related_name='categories')
    title = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='categories/', null=True, blank=True)

    def __str__(self):
        return self.title