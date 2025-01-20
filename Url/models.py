from django.db import models
import uuid
from django.contrib.auth.models import User

user = User()
class Click(models.Model):
    unique_code = models.UUIDField(default=uuid.uuid4, editable=False,unique=True)
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    url = models.URLField(unique=False)
    clicks = models.IntegerField(default=0)
    url_output = models.URLField(unique=False)

    def __str__(self):
        return f"{self.user.username} - {self.clicks} clicks"