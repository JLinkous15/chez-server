from django.db import models


class Like(models.Model):
    chef = models.ForeignKey(
        "Chef", on_delete=models.CASCADE, related_name="likers")
    chez = models.ForeignKey(
        "Chez", on_delete=models.CASCADE, related_name="liked_chezzes")
    date = models.DateTimeField(auto_now_add=True)
    like = models.BooleanField(null=True, blank=True)
