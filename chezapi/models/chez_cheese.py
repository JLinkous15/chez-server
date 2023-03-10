from django.db import models


class ChezCheese(models.Model):
    cheese = models.ForeignKey(
        "Cheese", on_delete=models.CASCADE, related_name="cheeses")
    chez = models.ForeignKey(
        "Chez", on_delete=models.CASCADE, related_name="chezzes")
