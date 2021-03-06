# -*- coding: utf-8 -*-
from django.db import models
import os


def get_upload_path(instance, filename): 
    if instance.path == "." or instance.path == "":
        return os.path.join("%s" % instance.username, "%s" % instance.file_name)
    return os.path.join("%s" % instance.username, "%s" % instance.path, instance.file_name)


class UploadModel(models.Model):
    username = models.TextField()
    path = models.TextField()
    file_name = models.TextField()
    size = models.IntegerField()
    password = models.TextField()
    file = models.FileField(upload_to=get_upload_path)

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = UploadModel.objects.filter(pk=self.pk)[0]
            if this.file != self.file:
                this.file.delete(save=False)
        except: pass # when new file then we do nothing, normal case
        super(UploadModel, self).save(*args, **kwargs)