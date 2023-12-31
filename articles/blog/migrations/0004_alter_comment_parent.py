# Generated by Django 4.2.1 on 2023-12-26 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0003_comment_parent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="replies",
                to="blog.comment",
            ),
        ),
    ]
