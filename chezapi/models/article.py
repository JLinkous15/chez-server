from django.db import models


class Article(models.Model):
    chef = models.ForeignKey(
        "Chef", on_delete=models.CASCADE, related_name="articles")
    title = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=5000)
    image = models.ImageField(null=True, blank=True)
