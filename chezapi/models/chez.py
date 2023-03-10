from django.db import models


class Chez(models.Model):
    chef = models.ForeignKey("Chef", on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    recipe = models.CharField(max_length=1000)
    image = models.ImageField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
