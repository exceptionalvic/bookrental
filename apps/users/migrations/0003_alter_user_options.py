# Generated by Django 3.2.18 on 2024-03-16 21:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20240314_1754'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('date_joined',)},
        ),
    ]