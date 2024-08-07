from django import forms
from django.db.models import Q, Prefetch
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django_select2 import forms as s2forms

from guide.models import Step, Answer, Question, Feeling, AnswerStatus, AnswerStatuses, Section, AnswerVote, \
    Sect


class StepListView(ListView):
    model = Step

    def get_queryset(self):
        return super().get_queryset().filter(sect=self.kwargs.get('sect').upper())#.with_answer_count(self.request.user)

    def get_context_data(self, **kwargs):
        sect = get_object_or_404(Sect, pk=self.kwargs.get('sect').upper())
        context = super().get_context_data(**kwargs)
        context['sect'] = sect
        context['metadata'] = sect.get_metadata()
        return context


class QuestionListView(ListView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['step'] = get_object_or_404(Step, pk=self.kwargs.get('pk'))
        context['step'] = get_object_or_404(Step, sect=self.kwargs.get('sect'), number=self.kwargs.get('step'))
        context['metadata'] = context['step'].get_metadata()
        return context

    def get_queryset(self):
        # qs = super().get_queryset().select_related('section').filter(section__step_id=self.kwargs.get('pk'))
        qs = super().get_queryset().select_related('section').filter(
            section__step__sect_id=self.kwargs.get('sect'),
            section__step__number=self.kwargs.get('step')
        )
        if self.request.user.is_authenticated:
            qs = qs.with_answer_count(self.request.user)
        qs = qs.order_by('section__step__number', 'section__number', 'number')
        return qs


# class SectionListView(ListView):
#     model = Section
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['step'] = get_object_or_404(Step, pk=self.kwargs.get('pk'))
#         context['metadata'] = context['step'].get_metadata()
#         return context
#
#     def get_queryset(self):
#         qs = super().get_queryset().filter(step_id=self.kwargs.get('pk'))
#         if self.request.user.is_authenticated:
#             qs = qs.prefetch_related(Prefetch('question_set', queryset=Question.objects.with_answer_count(self.request.user).order_by('number')))
#             # for section in qs:
#             #     section.questions = section.question_set.all().with_answer_count(self.request.user)
#         else:
#             qs = qs.prefetch_related('question_set')
#         return qs


class SectionDetailView(DetailView):
    model = Section

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['metadata'] = self.object.get_metadata()
        return context

    def get_object(self, queryset=None):
        # self.object = super().get_object(queryset)
        self.object = get_object_or_404(
            Section,
            step__sect_id=self.kwargs.get('sect'),
            step__number=self.kwargs.get('step'),
            number=self.kwargs.get('section')
        )
        if self.request.user.is_authenticated:
            self.object.questions = self.object.question_set.all().with_answer_count(self.request.user).order_by('number')
        return self.object


class FeelingsWidget(s2forms.ModelSelect2TagWidget):
    search_fields = [
        "title__icontains",
    ]

    queryset = Feeling.objects.all()

    def get_queryset(self):
        return self.queryset.filter(Q(user=None) | Q(user=self.user))

    def value_from_datadict(self, data, files, name):
        '''Create objects for given non-pimary-key values. Return list of all primary keys.'''
        values = set(super().value_from_datadict(data, files, name))
        pks = self.get_queryset().filter(**{'pk__in': [val for val in values if val.isnumeric()]}).values_list('pk', flat=True)
        pks = set(map(str, pks))
        cleaned_values = list(pks)
        for val in values - pks:
            cleaned_values.append(Feeling.objects.create(title=val, user=self.user).pk)
        return cleaned_values


class AnswerFormMixin:
    model = Answer
    fields = ['situation', 'thoughts', 'feelings', 'actions', 'publish']

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        if self.request.user.is_authenticated:
            qs = Feeling.objects.filter(Q(user=None) | Q(user=self.request.user))
        else:
            qs = Feeling.objects.filter(user=None)
        form.fields['feelings'] = forms.ModelMultipleChoiceField(
            label='Чувства', queryset=qs,
            widget=FeelingsWidget, required=False
        )
        form.fields['feelings'].widget.user = self.request.user
        return form


class AnswerCreateView(AnswerFormMixin, CreateView):

    def get_question(self):
        return get_object_or_404(
            Question.objects.select_related('section', 'section__step'),
            section__step__sect_id=self.kwargs.get('sect'),
            section__step__number=self.kwargs.get('step'),
            section__number=self.kwargs.get('section'),
            number=self.kwargs.get('question')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['question'] = get_object_or_404(Question.objects.select_related('section', 'section__step'), pk=self.kwargs.get('pk'))
        context['question'] = self.get_question()
        context['metadata'] = context['question'].get_metadata()
        context['examples'] = context['question'].get_examples(user=self.request.user if self.request.user.is_authenticated else None)
        if self.request.user.is_authenticated:
            context['show_close_button'] = True
            context['is_closed'] = context['question'].answerstatus_set.filter(
                status=AnswerStatuses.COMPLETED, user=self.request.user
            )
            context['answers'] = Answer.objects.filter(
                question=context['question'], user=self.request.user, show_on_site=False
            )
        return context

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            raise PermissionDenied()
        self.object = form.save(commit=False)
        self.object.question = self.get_question()
        self.object.user = self.request.user
        self.object.save()
        form.save_m2m()
        AnswerStatus.objects.get_or_create(user=self.request.user, question=self.object.question)
        return HttpResponseRedirect(self.object.question.get_absolute_url())


class AnswerUpdateView(AnswerFormMixin, LoginRequiredMixin, UpdateView):

    def get_object(self, queryset=None):
        self.object = super().get_object()
        if self.object.user != self.request.user or self.object.show_on_site:
            raise PermissionDenied()
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = self.object.question
        context['metadata'] = context['question'].get_metadata()
        return context

    def get_success_url(self):
        return self.object.question.get_absolute_url()


class AnswerDeleteView(LoginRequiredMixin, DeleteView):
    model = Answer

    def get_object(self, queryset=None):
        self.object = super().get_object()
        if self.object.user != self.request.user or self.object.show_on_site:
            raise PermissionDenied()
        return self.object

    def get_success_url(self):
        return self.object.question.get_absolute_url()


class AnswerCloseView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        question = get_object_or_404(Question, pk=self.kwargs.get('pk'))
        answerstatus, _ = AnswerStatus.objects.get_or_create(user=self.request.user, question=question)
        if answerstatus.status == AnswerStatuses.COMPLETED:
            answerstatus.status = AnswerStatuses.WORK
        else:
            answerstatus.status = AnswerStatuses.COMPLETED
        answerstatus.save()
        return HttpResponseRedirect(question.get_absolute_url())


class AnswerVoteView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        val = 1 if self.kwargs.get('vote') == 'up' else -1
        answer = get_object_or_404(Answer, pk=self.kwargs.get('pk'))
        vote, created = AnswerVote.objects.get_or_create(answer=answer, user=self.request.user)
        if not created and vote.vote == val:
            vote.delete()
        else:
            vote.vote = val
            vote.save()
        return HttpResponseRedirect(answer.question.get_absolute_url())
