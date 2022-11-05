from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView

from guide.models import Step, Answer, Question


class StepListView(LoginRequiredMixin, ListView):
    model = Step

    def get_queryset(self):
        program = self.kwargs.get('program').upper()
        if program not in ('AA', 'NA'):
            raise Http404
        return super().get_queryset().filter(program=program).with_answer_count(self.request.user)


class QuestionListView(LoginRequiredMixin, ListView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step'] = get_object_or_404(Step, pk=self.kwargs.get('pk'))
        return context

    def get_queryset(self):
        return super().get_queryset().filter(step_id=self.kwargs.get('pk')).with_answer_count(self.request.user)


class AnswerCreateView(LoginRequiredMixin, CreateView):
    model = Answer
    fields = ['situation', 'thoughts', 'feelings', 'actions']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = get_object_or_404(Question, pk=self.kwargs.get('pk'))
        context['answers'] = Answer.objects.filter(question=context['question'], user=self.request.user)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.question = get_object_or_404(Question, pk=self.kwargs.get('pk'))
        self.object.user = self.request.user
        self.object.save()
        form.save_m2m()
        return HttpResponseRedirect(self.request.path)
