from django.db import models


class Subscribe(models.Model):
    chef = models.ForeignKey(
        "Chef", on_delete=models.CASCADE, related_name="subscribed_to")
    subscriber = models.ForeignKey(
        "Chef", on_delete=models.CASCADE, related_name="subscribers")
    date = models.DateField(auto_now=False, auto_now_add=True)

    # consider related_names for each foreign key in the project after lunch
