# Generated by Django 4.1.1 on 2023-06-15 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("addresses", "0003_address_city_address_map_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="address",
            name="address2",
            field=models.CharField(default="Canada", max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="address",
            name="country",
            field=models.CharField(default="Canada", max_length=30),
            preserve_default=False,
        ),
    ]