# Generated by Django 4.0.4 on 2022-07-13 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_account_referel_activated_account_referel_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
    ]
