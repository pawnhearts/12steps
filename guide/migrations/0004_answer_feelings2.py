# Generated by Django 4.1.3 on 2022-11-05 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("guide", "0003_alter_answer_options_answer_created"),
    ]

    operations = [
        migrations.AddField(
            model_name="answer",
            name="feelings2",
            field=models.CharField(
                blank=True, max_length=512, null=True, verbose_name="Чувства"
            ),
        ),
    ]
