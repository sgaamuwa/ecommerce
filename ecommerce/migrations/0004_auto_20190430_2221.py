# Generated by Django 2.2 on 2019-04-30 19:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0003_auto_20190430_2147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='category',
            name='date_modified',
        ),
    ]
