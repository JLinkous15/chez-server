from django.db import models


class Comment(models.Model):
    chef = models.ForeignKey("Chef", on_delete=models.CASCADE)
    chez = models.ForeignKey(
        "Chez", on_delete=models.CASCADE, related_name="chez_comments")
    body = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True)
