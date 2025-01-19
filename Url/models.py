from django.db import models
import uuid

class Click(models.Model):
    url = models.URLField(unique=True)
    clicks = models.IntegerField(default=0)
    unique_code = models.UUIDField(default=uuid.uuid4, editable=False,unique=True)

    def __str__(self):
        return f"{self.url} - {self.clicks} clicks"