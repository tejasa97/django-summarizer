# Generated by Django 3.1.4 on 2021-01-02 10:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('summarizer_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='summary',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='summaries', to=settings.AUTH_USER_MODEL),
        ),
    ]
