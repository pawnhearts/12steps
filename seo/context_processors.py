from django.db.models.functions import Length

from seo.models import MetaData


def metadata(request):
    paths = []
    elems = request.path.rstrip('/').split('/')
    while elems:
        paths.append('/'.join(elems)+'/')
        elems.pop()
    return {'metadata': MetaData.objects.filter(url__in=paths).order_by(Length('url')).reverse().first()}
