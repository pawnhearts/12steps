# Generated by Django 4.1.3 on 2022-11-12 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("guide", "0012_remove_section_show_header"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="section",
            name="text",
        ),
    ]