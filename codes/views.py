from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from codes.models import Barcode, Image, Tag, BarcodeHasTag
from django.views import defaults
import magic
import re

from .forms import BarcodeEditForm


def index(request):
    return HttpResponse(render(request, 'codes/index.html'))


def img(request, filename):
    try:
        im = Image.objects.get(name=filename)
        type = magic.detect_from_fobj(im.file).mime_type
        return HttpResponse(im.file, content_type=type)
    except Image.DoesNotExist:
        return defaults.page_not_found(request, None)


def barcodes_index(request):
    barcodes = Barcode.objects.all()
    context = {'barcodes': barcodes}
    return HttpResponse(render(request, 'codes/barcodes/barcodes.html', context))


def barcodes_edit(request, short):
    try:
        barcode = Barcode.objects.get(short=short) if short != 'new' else Barcode()
    except Barcode.DoesNotExist:
        barcode = None
    if request.method == 'POST':
        form = BarcodeEditForm(request.POST)
        if barcode is None:
            form.add_error(None, 'I can\'t find that code anymore :(')
        if form.is_valid():
            barcode.short = re.sub(r'\W+', '', form.cleaned_data['name'].lower().replace(' ', '_'))
            barcode.name = form.cleaned_data['name']
            barcode.description = form.cleaned_data['description']
            barcode.resources = form.cleaned_data['resources']
            for tag in barcode.tags.all():
                barcode.tags.remove(tag)
            for tag in form.cleaned_data['tags']:
                barcode.tags.add(tag)
            barcode.save()
            for image in request.FILES.getlist('images'):
                im = Image(file=image, name=image.name, belongs_to=barcode)
                im.save()
            return HttpResponse('ok')
    else:
        if barcode is None:
            return defaults.page_not_found(request, None)
        form = BarcodeEditForm(initial={
            'name': barcode.name,
            'description': barcode.description,
            'resources': barcode.resources,
            'tags': [tag for tag in barcode.tags.all()]
        })
    context = {'short': short, 'barcode': barcode, 'form': form}
    return HttpResponse(render(request, 'codes/barcodes/edit.html', context))
