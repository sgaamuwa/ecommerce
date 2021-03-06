# Generated by Django 2.2 on 2019-05-04 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0013_auto_20190502_1945'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shoppingcart',
            old_name='item_id',
            new_name='shopping_cart_id',
        ),
        migrations.RemoveField(
            model_name='shoppingcart',
            name='added_on',
        ),
        migrations.RemoveField(
            model_name='shoppingcart',
            name='attributes',
        ),
        migrations.RemoveField(
            model_name='shoppingcart',
            name='products',
        ),
        migrations.RemoveField(
            model_name='shoppingcart',
            name='quantity',
        ),
        migrations.CreateModel(
            name='ShoppingCartItem',
            fields=[
                ('item_id', models.AutoField(primary_key=True, serialize=False)),
                ('attributes', models.CharField(blank=True, max_length=1000, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.Product')),
                ('shopping_cart_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart_items', to='ecommerce.ShoppingCart')),
            ],
        ),
    ]
