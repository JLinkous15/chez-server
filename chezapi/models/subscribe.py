from django.db import models


class Subscribe(models.Model):
    chef = models.ForeignKey(
        "Chef", on_delete=models.CASCADE, related_name="chef_subscribed_to")
    subscriber = models.ForeignKey(
        "Chef", on_delete=models.CASCADE, related_name="chef_subscribers")
    date = models.DateField(auto_now=False, auto_now_add=True)
