from django.contrib import admin
from django.urls import reverse
from guide.models import Step, Question, Answer, Feeling, Section
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE


class TinyMCEFlatPageAdmin(FlatPageAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "content":
            return db_field.formfield(
                widget=TinyMCE(
                    attrs={"cols": 80, "rows": 30},
                    mce_attrs={"external_link_list_url": reverse("tinymce-linklist")},
                )
            )
        return super().formfield_for_dbfield(db_field, **kwargs)


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, TinyMCEFlatPageAdmin)


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ('number', 'title')
    list_filter = ('program',)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('number', 'title')
    list_filter = ('step__program', 'step')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    list_filter = ('section__step__program', 'section__step', 'section')


@admin.register(Feeling)
class FeelingAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question')
    list_filter = ('user',)
    filter_horizontal = ('feelings',)
