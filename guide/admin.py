from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin
from guide.models import Step, Question, Answer, Feeling


@admin.register(Step)
class StepAdmin(OrderedModelAdmin):
    list_display = ('title', 'move_up_down_links')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('step', 'number')
    list_filter = ('step',)


@admin.register(Feeling)
class FeelingAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question')
    list_filter = ('user',)
