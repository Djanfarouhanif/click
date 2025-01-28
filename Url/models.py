from django.db import models
import uuid
from django.contrib.auth.models import User


class Click(models.Model):
    unique_code = models.UUIDField(default=uuid.uuid4, editable=False,unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link_name = models.CharField(max_length=200)
    url = models.URLField(unique=False)
    clicks = models.IntegerField(default=0)
    url_output = models.URLField(unique=False)

    def __str__(self):
        return f"{self.user.username} - {self.clicks} clicks"