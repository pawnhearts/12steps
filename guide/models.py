from django.contrib.auth.models import User
from django.db import models
from ordered_model.models import OrderedModel


class Step(OrderedModel):
    title = models.CharField('Название', max_length=255)
    text = models.TextField('Текст', blank=True, null=True)

    def __str__(self):
        return f'{self.order}. {self.title}'

    class Meta:
        verbose_name = "Шаг"
        verbose_name_plural = "Шаги"
        ordering = ['order']


class Question(OrderedModel):
    step = models.ForeignKey(Step, verbose_name='Шаг', on_delete=models.CASCADE)
    text = models.TextField('Текст вопроса', blank=True, null=True)

    def __str__(self):
        return f'{self.step.order}. {self.order}'

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ['order']


class Feeling(models.Model):
    title = models.CharField('Чуство', max_length=255)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Чувсто"
        verbose_name_plural = "Чувства"


class Answer(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name='Вопрос', on_delete=models.CASCADE)
    situation = models.TextField('Ситуация', blank=True, null=True)
    thoughts = models.TextField('Мысли', blank=True, null=True)
    actions = models.TextField('Действия', blank=True, null=True)
    feelings = models.ManyToManyField(Feeling, blank=True, verbose_name='Чувства')

    def __str__(self):
        return f'{self.user} {self.question}'

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
