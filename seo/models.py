from django.db import models


class MetaData(models.Model):
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=68, null=True, blank=True)
    description = models.CharField(max_length=155, null=True, blank=True)
    keywords = models.CharField(max_length=255, null=True, blank=True)
    h1 = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = 'Мета теги'
        verbose_name_plural = 'Мета теги'


class MetaDataBase(models.Model):
    seo_title = models.CharField(max_length=68, null=True, blank=True)
    seo_description = models.CharField(max_length=155, null=True, blank=True)
    seo_keywords = models.CharField(max_length=255, null=True, blank=True)
    seo_h1 = models.CharField(max_length=255, null=True, blank=True)

    def get_metadata(self):
        return {k: getattr(self, f'seo_{k}') for k in ('title', 'description', 'keywords', 'h1')}

    class Meta:
        abstract = True
