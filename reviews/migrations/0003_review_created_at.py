# Generated by Django 4.1.1 on 2022-10-04 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reviews", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, default="2022-09-09"),
            preserve_default=False,
        ),
    ]
