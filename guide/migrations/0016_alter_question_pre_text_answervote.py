# Generated by Django 4.1.3 on 2022-11-13 06:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("guide", "0015_alter_question_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="pre_text",
            field=tinymce.models.HTMLField(
                blank=True, null=True, verbose_name="Текст перед вопросом"
            ),
        ),
        migrations.CreateModel(
            name="AnswerVote",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "vote",
                    models.SmallIntegerField(default=1, verbose_name="Голосование"),
                ),
                (
                    "answer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="guide.answer",
                        verbose_name="Ответ",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Голос за ответ",
                "verbose_name_plural": "Голоса за ответа",
            },
        ),
    ]
