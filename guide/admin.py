from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin
from guide.models import Step, Question, Answer, Feeling


@admin.site.register(Step)
class StepAdmin(OrderedModelAdmin):
    list_display = ('title', 'move_up_down_links')


@admin.site.register(Question)
class QuestionAdmin(OrderedModelAdmin):
    list_display = ('__str__', 'move_up_down_links')
    list_filter = ('step',)


@admin.site.register(Feeling)
class FeelingAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.site.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question')
    list_filter = ('user',)
