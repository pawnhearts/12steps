from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Subquery, OuterRef
from ordered_model.models import OrderedModel


class StepQuerySet(models.QuerySet):
    def with_answer_count(self, user):
        sq = Subquery(Answer.objects.filter(question__step=OuterRef('pk'), user=user).values('id'))
        return self.annotate(answer_count=Count(sq))


class Programs(models.TextChoices):
    NA = 'NA', 'АН'
    AA = 'AA', 'АА'


class Step(models.Model):
    objects = StepQuerySet.as_manager()

    program = models.CharField('Программа', max_length=4, choices=Programs.choices, default=Programs.NA)
    number = models.PositiveSmallIntegerField('Номер')
    title = models.CharField('Название', max_length=255)
    text = models.TextField('Текст', blank=True, null=True)

    def __str__(self):
        return f'{self.get_program_display()}. Шаг {self.number}. {self.title}'

    def save(self, **kwargs):
        if not self.number:
            self.number = (Step.objects.filter(program=self.program).aggregate(n=models.Max('number'))['n'] or 0) + 1
        super().save(**kwargs)

    class Meta:
        verbose_name = "Шаг"
        verbose_name_plural = "Шаги"
        ordering = ['number']


class QuestionQuerySet(models.QuerySet):
    def with_answer_count(self, user):
        sq = Subquery(Answer.objects.filter(question=OuterRef('pk'), user=user).values('id'))
        return self.annotate(answer_count=Count(sq))


class Question(models.Model):
    objects = QuestionQuerySet.as_manager()

    step = models.ForeignKey(Step, verbose_name='Шаг', on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField('Номер')
    # title = models.CharField('Заголовок', max_length=512, blank=True, null=True)
    text = models.TextField('Текст вопроса', blank=True, null=True)

    def __str__(self):
        return f'{self.step.get_program_display()}. Шаг {self.step.number}. Вопрос {self.number}'

    def save(self, **kwargs):
        if not self.number:
            self.number = (Question.objects.filter(step=self.step).aggregate(n=models.Max('number'))['n'] or 0) + 1
        super().save(**kwargs)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ['number']


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
