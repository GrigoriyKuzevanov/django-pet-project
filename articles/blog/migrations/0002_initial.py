# Generated by Django 4.2.1 on 2023-12-22 09:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("blog", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="author",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="posts",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="posts",
                to="blog.category",
                verbose_name="Категория",
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="tags",
            field=models.ManyToManyField(
                blank=True, related_name="tags", to="blog.tagpost", verbose_name="Тэги"
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="post",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="blog.post",
            ),
        ),
        migrations.AddIndex(
            model_name="post",
            index=models.Index(
                fields=["-time_create"], name="blog_post_time_cr_cc1db6_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="comment",
            index=models.Index(
                fields=["-time_create"], name="blog_commen_time_cr_0f1602_idx"
            ),
        ),
    ]