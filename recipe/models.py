from django.db import models
from django.conf import settings

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='recipes/')
    description = models.TextField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='recipes'
    )

    def __str__(self):
        return self.name
