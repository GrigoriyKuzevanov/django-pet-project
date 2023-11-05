from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse


class PublishedManager(models.Manager):
    """
    Пользовательский менеджер, который возвращает
    только посты, с полем is_published=1
    """
    
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Post.Status.PUBLISHED)


class Post(models.Model):
    """
    Модель записи в блоге
    """
    class Status(models.IntegerChoices):
        """
        Класс выбора значений для каждого поста,
        0, 1 - значения заносятся в базу данных (Post.Status.values)
        'Черновик', 'Опубликовано' - метки (Post.Status.labels)
        """

        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'


    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts')
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags')

    objects = models.Manager()      # менеджер модели по умолчанию
    published = PublishedManager()  # пользовательский менеджер модели

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})
    
    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]


class Category(models.Model):
    """
    Модель категории записи в блоге
    """
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})  # функция reverse возвращает url с name='category'
    

class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag
    
    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})
