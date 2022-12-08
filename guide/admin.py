from django.contrib import admin
from django.db.models import Sum
from django.urls import reverse
from guide.models import Step, Question, Answer, Feeling, Section, Sect
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


class SectionInlineAdmin(admin.StackedInline):
    model = Section
    exclude = ['seo_title', 'seo_description', 'seo_keywords', 'seo_h1']


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ('number', 'title')
    list_filter = ('sect',)
    inlines = (SectionInlineAdmin,)


class QuestionInlineAdmin(admin.StackedInline):
    model = Question
    exclude = ['seo_title', 'seo_description', 'seo_keywords', 'seo_h1']


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('number', 'title')
    list_filter = ('step__sect', 'step')
    inlines = (QuestionInlineAdmin,)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    list_filter = ('section__step__sect', 'section__step', 'section')


@admin.register(Feeling)
class FeelingAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'publish', 'show_on_site', 'rating')
    list_filter = ('user', 'publish', 'show_on_site')
    filter_horizontal = ('feelings',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(publish=True)

    def rating(self, obj):
        return obj.answervote_set.aggregate(rating=Sum('vote', default=0))['rating']


admin.site.register(Sect)
