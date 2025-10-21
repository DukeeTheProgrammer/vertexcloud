from django.db import models
from datetime import datetime
from django.conf import settings


class File(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to="static/files")
    created_at = models.DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return self.file.name

