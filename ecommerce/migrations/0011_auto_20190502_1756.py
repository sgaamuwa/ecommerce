# Generated by Django 2.2 on 2019-05-02 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0010_auto_20190502_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingcart',
            name='attributes',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]