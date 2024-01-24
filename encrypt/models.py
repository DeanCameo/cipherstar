from django.db import models

class EncryptedText(models.Model):
    text = models.TextField()
    shift = models.PositiveSmallIntegerField()

