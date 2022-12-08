from seo.models import MetaData


def metadata(request):
    return {'metadata': MetaData.objects.filter(url=request.path).first()}
