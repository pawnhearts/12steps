from guide.models import Programs


def programs(request):
    return {'programs': Programs.choices}
