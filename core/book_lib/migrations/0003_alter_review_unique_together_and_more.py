# Generated by Django 4.2.16 on 2024-09-18 12:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book_lib', '0002_alter_review_book'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('user', 'book')},
        ),
        migrations.AddIndex(
            model_name='book',
            index=models.Index(fields=['title', 'author'], name='book_lib_bo_title_f83735_idx'),
        ),
    ]
