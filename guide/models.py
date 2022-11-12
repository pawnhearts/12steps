from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Q, Subquery, OuterRef
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

    def save(self, **kwargs):
        if not self.number:
            self.number = (Step.objects.filter(program=self.program).aggregate(n=models.Max('number'))['n'] or 0) + 1
        super().save(**kwargs)

    class Meta:
        verbose_name = "Шаг"
        verbose_name_plural = "Шаги"
        ordering = ['number']


class Section(models.Model):
    step = models.ForeignKey(Step, verbose_name='Шаг', on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField('Номер', blank=True, db_index=True)
    show_header = models.BooleanField('Показывать заголовок', default=True)
    title = models.CharField('Название', max_length=256)
    text = HTMLField('Текст', blank=True, null=True)

    def __str__(self):
        return f'{self.step.get_program_display()}. Шаг {self.step.number}. {self.title}'

    def save(self, **kwargs):
        if not self.number:
            self.number = (Section.objects.filter(step=self.step).aggregate(n=models.Max('number'))['n'] or 0) + 1
        super().save(**kwargs)

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"
        ordering = ['step__number', 'number']


class QuestionQuerySet(models.QuerySet):
    def with_answer_count(self, user):
        sq = Subquery(AnswerStatus.objects.filter(question_id=OuterRef('pk'), user=user).values('status')[:1])
        return self.annotate(answer_count=Count('answer', filter=Q(answer__user=user)), status=sq)


class Question(models.Model):
    objects = QuestionQuerySet.as_manager()

    section = models.ForeignKey(Section, verbose_name='Раздел', on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField('Номер', blank=True, db_index=True)
    # title = models.CharField('Заголовок', max_length=512, blank=True, null=True)
    text = HTMLField('Текст вопроса', blank=True, null=True)

    def __str__(self):
        return f'{self.section.step.get_program_display()}. Шаг {self.section.step.number}. Раздел {self.section.title}. Вопрос {self.number}'

    def save(self, **kwargs):
        if not self.number:
            self.number = (Question.objects.filter(section=self.section).aggregate(n=models.Max('number'))['n'] or 0) + 1
        super().save(**kwargs)

    def get_examples(self):
        return self.answer_set.filter(publish=True, show_on_site=True)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ['section__step__number', 'section__number', 'number']


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
    publish = models.BooleanField('Опубликовать в примерах', default=False, db_index=True, help_text='Опубликовать в примерах')
    show_on_site = models.BooleanField('Прошло модерацию', default=False)

    def __str__(self):
        return f'{self.user} {self.question}'

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
