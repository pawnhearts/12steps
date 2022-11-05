# Generated by Django 4.1.3 on 2022-11-05 20:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("guide", "0002_alter_question_options_alter_section_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="answer",
            options={
                "ordering": ["created"],
                "verbose_name": "Ответ",
                "verbose_name_plural": "Ответы",
            },
        ),
        migrations.AddField(
            model_name="answer",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="Дата и время",
            ),
            preserve_default=False,
        ),
    ]
