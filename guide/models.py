from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Q, Subquery, OuterRef
from django.urls import reverse
from tinymce.models import HTMLField


class StepQuerySet(models.QuerySet):
    def with_answer_count(self, user):
        return self.annotate(
            answer_count=Count('section__question__answer', filter=Q(section__question__answer__user=user))
        )


class Programs(models.TextChoices):
    NA = 'NA', 'Шаги АН по руководству'
    AA = 'AA', 'Шаги АА'


class Step(models.Model):
    objects = StepQuerySet.as_manager()

    program = models.CharField('Программа', max_length=4, choices=Programs.choices, default=Programs.NA)
    number = models.PositiveSmallIntegerField('Номер', blank=True, db_index=True)
    title = models.CharField('Название', max_length=255)
    text = HTMLField('Текст', blank=True, null=True)

    def __str__(self):
        return f'{self.get_program_display()}. Шаг {self.number}. {self.title}'

    def get_absolute_url(self):
        return reverse('question-list', args=[self.pk])

    def save(self, **kwargs):
        if not self.number:
            self.number = (Step.objects.filter(program=self.program).aggregate(n=models.Max('number'))['n'] or 0) + 1
        super().save(**kwargs)

    class Meta:
        verbose_name = "Шаг"
        verbose_name_plural = "Шаги"
        ordering = ['number']
        # unique_together = [['program', 'number']]


class Section(models.Model):
    step = models.ForeignKey(Step, verbose_name='Шаг', on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField('Номер', blank=True, db_index=True)
    title = models.CharField('Название', max_length=256)
    # text = HTMLField('Текст', blank=True, null=True)

    def __str__(self):
        return f'{self.step.get_program_display()}. Шаг {self.step.number}. {self.title}'

    def get_absolute_url(self):
        return reverse('section-detail', args=[self.pk])

    def save(self, **kwargs):
        if not self.number:
            self.number = (Section.objects.filter(step=self.step).aggregate(n=models.Max('number'))['n'] or 0) + 1
        super().save(**kwargs)

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"
        ordering = ['step__number', 'number']
        # unique_together = [['step', 'number']]


class QuestionQuerySet(models.QuerySet):
    def with_answer_count(self, user):
        sq = Subquery(AnswerStatus.objects.filter(question_id=OuterRef('pk'), user=user).values('status')[:1])
        return self.annotate(answer_count=Count('answer', filter=Q(answer__user=user)), status=sq)


class Question(models.Model):
    objects = QuestionQuerySet.as_manager()

    section = models.ForeignKey(Section, verbose_name='Раздел', on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField('Номер', blank=True, db_index=True)
    # title = models.CharField('Заголовок', max_length=512, blank=True, null=True)
    text = models.TextField('Текст вопроса', blank=True, null=True)
    pre_text = HTMLField('Текст перед вопросом', blank=True, null=True)
    post_text = HTMLField('Текст после вопроса', blank=True, null=True)

    def __str__(self):
        return f'{self.section.step.get_program_display()}. Шаг {self.section.step.number}. Раздел {self.section.title}. Вопрос {self.number}'

    def get_absolute_url(self):
        return reverse('answer-create', args=[self.pk])

    def save(self, **kwargs):
        if self.pre_text and not BeautifulSoup(self.pre_text, features="html.parser").text.strip():
            self.pre_text = None
        if self.post_text and not BeautifulSoup(self.post_text, features="html.parser").text.strip():
            self.post_text = None
        if not self.number:
            self.number = (Question.objects.filter(section=self.section).aggregate(n=models.Max('number'))['n'] or 0) + 1
        super().save(**kwargs)

    def get_examples(self, user=None):
        qs = self.answer_set.filter(publish=True, show_on_site=True).annotate(
            rating=models.Sum('answervote__vote', default=0),
            votes_yes=models.Count('answervote', filter=Q(answervote__vote=1)),
            votes_no=models.Count('answervote', filter=Q(answervote__vote=-1)),
        ).order_by('-rating')
        if user:
            qs = qs.annotate(vote=Subquery(AnswerVote.objects.filter(answer=OuterRef('pk'), user=user).values('vote')[:1]))
        return qs

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ['section__step__number', 'section__number', 'number']
        # unique_together = [['section', 'number']]


class Feeling(models.Model):
    title = models.CharField('Чуство', max_length=255)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Чувсто"
        verbose_name_plural = "Чувства"


class Answer(models.Model):
    created = models.DateTimeField('Дата и время', auto_now_add=True, editable=False, db_index=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name='Вопрос', on_delete=models.CASCADE)
    situation = models.TextField('Ситуация', blank=True, null=True)
    thoughts = models.TextField('Мысли', blank=True, null=True)
    actions = models.TextField('Действия', blank=True, null=True)
    feelings = models.ManyToManyField(Feeling, blank=True, verbose_name='Чувства')
    publish = models.BooleanField('Опубликовать', default=False, db_index=True, help_text='Опубликовать свой пример для помощи другим зависимым с пониманием вопроса')
    show_on_site = models.BooleanField('Прошло модерацию', default=False)

    def __str__(self):
        return f'{self.user} {self.question}'

    def get_absolute_url(self):
        return reverse('answer-update', args=[self.pk])

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
        ordering = ['created']


class AnswerStatuses(models.TextChoices):
    WORK = 'WORK', 'В работе'
    COMPLETED = 'COMPLETED', 'Завершен'


class AnswerStatus(models.Model):
    created = models.DateTimeField('Дата и время', auto_now_add=True, editable=False)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name='Вопрос', on_delete=models.CASCADE)
    status = models.CharField('Статус', max_length=16, choices=AnswerStatuses.choices, default=AnswerStatuses.WORK)

    def __str__(self):
        return self.get_status_display()

    class Meta:
        verbose_name = "Статус ответа"
        verbose_name_plural = "Статусы ответа"


class AnswerVote(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, verbose_name='Ответ', on_delete=models.CASCADE)
    vote = models.SmallIntegerField('Голосование', default=1)

    def __str__(self):
        return f'{self.user} {self.answer} {self.vote}'

    class Meta:
        verbose_name = "Голос за ответ"
        verbose_name_plural = "Голоса за ответа"
