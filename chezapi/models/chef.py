from django.db import models
from django.contrib.auth.models import User


class Chef(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField()
    bio = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    subscriptions = models.ManyToManyField(
        "Chef", through="Subscribe")

    @property
    def username(self):
        return self.user.username

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def is_chef(self):
        return self.__chef

    @is_chef.setter
    def is_chef(self, value):
        self.__chef = value
