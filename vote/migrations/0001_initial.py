# Generated by Django 3.2.9 on 2021-12-29 07:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('pubdate', models.DateTimeField()),
                ('content', models.TextField()),
                ('voter', models.ManyToManyField(blank=True, related_name='voter', to=settings.AUTH_USER_MODEL)),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vwriter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('pic', models.ImageField(upload_to='vote/%y')),
                ('comment', models.TextField()),
                ('choicer', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vote.topic')),
            ],
        ),
    ]
