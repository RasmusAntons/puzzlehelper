from django.db import models
import uuid
import os


class Tag(models.Model):
    name = models.CharField(max_length=255)
    barcodes = models.ManyToManyField('Barcode', through='BarcodeHasTag')

    def __str__(self):
        return self.name


class Barcode(models.Model):
    short = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField()
    resources = models.TextField()
    tags = models.ManyToManyField(Tag, through='BarcodeHasTag')


def image_file_path(instance, filename):
    ext = filename.split('.')[-1] # todo: whitelist extensions
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('img', filename)


class Image(models.Model):
    file = models.ImageField(upload_to=image_file_path)
    name = models.CharField(max_length=255)
    belongs_to = models.ForeignKey(Barcode, on_delete=models.CASCADE)


class BarcodeHasTag(models.Model):
    barcode = models.ForeignKey(Barcode, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
