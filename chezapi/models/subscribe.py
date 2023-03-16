from django.db import models


class Subscribe(models.Model):
    chef = models.ForeignKey(
        "Chef", on_delete=models.CASCADE, related_name="logged_in_chef")
    chefscribed = models.ForeignKey(
        "Chef", on_delete=models.CASCADE, related_name="chefavorites")
    date = models.DateField(auto_now=False, auto_now_add=True)
