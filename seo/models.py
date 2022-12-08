from django.db import models


class MetaData(models.Model):
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=68, null=True, blank=True)
    description = models.CharField(max_length=155, null=True, blank=True)
    keywords = models.CharField(max_length=255, null=True, blank=True)
    h1 = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Мета теги'
        verbose_name_plural = 'Мета теги'
