# Generated by Django 4.0.4 on 2022-06-22 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_product_is_offer_active_product_product_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='offer_perc',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='offer_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
