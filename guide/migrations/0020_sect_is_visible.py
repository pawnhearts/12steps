# Generated by Django 4.1.3 on 2022-12-08 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("guide", "0019_remove_step_program"),
    ]

    operations = [
        migrations.AddField(
            model_name="sect",
            name="is_visible",
            field=models.BooleanField(
                default=False, verbose_name="Показывать на сайте"
            ),
        ),
    ]
