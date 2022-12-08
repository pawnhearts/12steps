from django.db.models.functions import Length

from seo.models import MetaData


def metadata(request):
    return {'metadata': MetaData.objects.filter(url=request.path).first()}
