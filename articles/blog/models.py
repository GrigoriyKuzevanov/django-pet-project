from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse
from slugify import slugify

from blog.tasks import resize_post_image


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

        DRAFT = 0, "Черновик"
        PUBLISHED = 1, "Опубликовано"

    title = models.CharField(
        max_length=255, verbose_name="Заголовок"
    )  # verbose_name отражается в админ панели, формах и др.
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="Слаг"
    )
    image = models.ImageField(
        upload_to="images/%Y/%m/%d/",
        default=None,
        blank=True,
        null=True,
        verbose_name="Картинка",
    )
    content = models.TextField(blank=True, verbose_name="Текст записи")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(
        choices=tuple(
            map(lambda x: (bool(x[0]), x[1]), Status.choices)
        ),  # в джанго нет BooleanChoices, map для преобразования
        default=Status.DRAFT,  # цифр 1, 0 в булевы значения True и False
        verbose_name="Опубликовано",
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,
        related_name="posts",
        verbose_name="Категория",
    )
    tags = models.ManyToManyField(
        "TagPost", blank=True, related_name="tags", verbose_name="Тэги"
    )
    # author = models.OneToOneField('Author', on_delete=models.SET_NULL, null=True, blank=True, related_name='posts_author', verbose_name='Автор')
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name="posts",
        null=True,
        default=None,
    )
    objects = models.Manager()  # менеджер модели по умолчанию
    published = PublishedManager()  # пользовательский менеджер модели

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post", kwargs={"post_slug": self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            resize_post_image.delay(self.image.path)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-time_create"]
        indexes = [models.Index(fields=["-time_create"])]


class Category(models.Model):
    """
    Модель категории записи в блоге
    """

    name = models.CharField(max_length=100, db_index=True, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "category", kwargs={"cat_slug": self.slug}
        )  # функция reverse возвращает url с name='category'


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True, verbose_name="Тэг")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse("tag", kwargs={"tag_slug": self.slug})

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"


# class Author(models.Model):
#     name = models.CharField(max_length=100)
#     age = models.IntegerField(null=True)
#     a_count = models.IntegerField(blank=True, default=0)

#     def __str__(self):
#         return self.name


class Comment(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
        null=True,
    )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="replies", null=True, blank=True
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments", null=True
    )
    text = models.TextField(
        max_length=2000, blank=False, verbose_name="Текст комментария"
    )
    time_create = models.DateTimeField(auto_now=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-time_create"]
        indexes = [models.Index(fields=["-time_create"])]

    def get_absolute_url(self):
        return reverse("post", kwargs={"post_slug": self.post.slug})


# class Reply(models.Model):
#     author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='authors', verbose_name='Автор')
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies', verbose_name='Ответ')
#     text = models.TextField(max_length=2000, blank=False, verbose_name='Текст ответа')
#     time_create = models.DateTimeField(auto_now=True, verbose_name='Дата создания')


class UploadFiles(models.Model):
    file = models.FileField(upload_to="uploads_model")
