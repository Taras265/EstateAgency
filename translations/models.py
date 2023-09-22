from django.db import models


class Translation(models.Model):
    slug = models.CharField(unique=True, max_length=100)

    ru = models.CharField(max_length=150)
    en = models.CharField(max_length=150)
    uk = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.slug} ({self.en}, {self.uk}, {self.ru})"
