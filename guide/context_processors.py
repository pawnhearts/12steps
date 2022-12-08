from guide.models import Sect


def sects(request):
    return {'sects': Sect.objects.all()}
