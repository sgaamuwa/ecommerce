# Generated by Django 2.2 on 2019-04-30 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_auto_20190429_1719'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='department',
            name='date_modified',
        ),
    ]