# Generated by Django 4.1.3 on 2022-12-08 00:09

from django.db import migrations


def create_root(*args):
    from seo.models import MetaData
    MetaData.objects.create(url='/')


class Migration(migrations.Migration):

    dependencies = [
        ("seo", "0001_initial"),
    ]

    operations = [migrations.RunPython(create_root)]
