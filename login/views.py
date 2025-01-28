from django.http import HttpResponse


def index(request):
    return HttpResponse("Test please work, literally if you don't I will cry")