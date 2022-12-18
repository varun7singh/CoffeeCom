# Generated by Django 4.1.4 on 2022-12-18 10:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('watchlist', '0002_alter_movies_splatform_reviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]