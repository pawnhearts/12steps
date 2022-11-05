from django.views.generic import ListView, UpdateView, DetailView

from guide.models import Step


class StepListView(ListView):
    model = Step


class StepDetailView(DetailView):
    model = Step
