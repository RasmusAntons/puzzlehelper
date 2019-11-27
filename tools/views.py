from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .forms import UrlfinderForm


def index(request):
    return HttpResponse(render(request, 'tools/index.html'))


def urlfinder(request):
    form = UrlfinderForm()
    context = {'form': form}
    return HttpResponse(render(request, 'tools/urlfinder.html', context))
