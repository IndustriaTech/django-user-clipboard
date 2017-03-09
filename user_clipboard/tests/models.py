from django.db import models


class ModelWithFile(models.Model):
    document = models.FileField(upload_to='documents', max_length=512)


class ModelWithImage(models.Model):
    image = models.ImageField(upload_to='images', max_length=512)
