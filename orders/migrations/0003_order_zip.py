# Generated by Django 4.0.4 on 2022-06-07 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_rename_addres_line_1_order_address_line_1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='zip',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
