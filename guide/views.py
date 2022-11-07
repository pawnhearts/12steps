from django import forms
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django_select2 import forms as s2forms

from guide.models import Step, Answer, Question, Feeling, AnswerStatus, AnswerStatuses


class StepListView(ListView):
    model = Step

    def get_queryset(self):
        program = self.kwargs.get('program').upper()
        if program not in ('AA', 'NA'):
            raise Http404()
        return super().get_queryset().filter(program=program)#.with_answer_count(self.request.user)


class QuestionListView(ListView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step'] = get_object_or_404(Step, pk=self.kwargs.get('pk'))
        return context

    def get_queryset(self):
        qs = super().get_queryset().filter(section__step_id=self.kwargs.get('pk'))
        if self.request.user.is_authenticated:
            qs = qs.with_answer_count(self.request.user)
        return qs


class FeelingsWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "title__icontains",
    ]


class AnswerCreateView(CreateView):
    model = Answer
    fields = ['situation', 'thoughts', 'feelings2', 'feelings', 'actions']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = get_object_or_404(Question, pk=self.kwargs.get('pk'))
        if self.request.user.is_authenticated:
            context['show_close_button'] = True
            context['is_closed'] = context['question'].answerstatus_set.filter(
                status=AnswerStatuses.COMPLETED, user=self.request.user
            )
            context['answers'] = Answer.objects.filter(question=context['question'], user=self.request.user)
        return context

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            raise PermissionDenied()
        self.object = form.save(commit=False)
        self.object.question = get_object_or_404(Question, pk=self.kwargs.get('pk'))
        self.object.user = self.request.user
        self.object.save()
        form.save_m2m()
        AnswerStatus.objects.get_or_create(user=self.request.user, question=self.object.question)
        return HttpResponseRedirect(self.request.path)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['feelings'] = forms.ModelMultipleChoiceField(
            label='Чувства', queryset=Feeling.objects.all(), widget=FeelingsWidget, required=False
        )
        return form


class AnswerUpdateView(LoginRequiredMixin, UpdateView):
    model = Answer
    fields = ['situation', 'thoughts', 'feelings2', 'feelings', 'actions']

    def get_object(self, queryset=None):
        self.object = super().get_object()
        if self.object.user != self.request.user:
            raise PermissionDenied()
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = self.object.question
        return context

    def get_success_url(self):
        return f'/questions/{self.object.question.pk}/'

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['feelings'] = forms.ModelMultipleChoiceField(
            label='Чувства', queryset=Feeling.objects.all(), widget=FeelingsWidget, required=False
        )
        return form


class AnswerDeleteView(LoginRequiredMixin, DeleteView):
    model = Answer

    def get_object(self, queryset=None):
        self.object = super().get_object()
        if self.object.user != self.request.user:
            raise PermissionDenied()
        return self.object

    def get_success_url(self):
        return f'/question/{self.object.question_id}/'


class AnswerCloseView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        question = get_object_or_404(Question, pk=self.kwargs.get('pk'))
        answerstatus, _ = AnswerStatus.objects.get_or_create(user=self.request.user, question=question)
        if answerstatus.status == AnswerStatuses.COMPLETED:
            answerstatus.status = AnswerStatuses.WORK
        else:
            answerstatus.status = AnswerStatuses.COMPLETED
        answerstatus.save()
        return HttpResponseRedirect(f'/question/{question.pk}/')
