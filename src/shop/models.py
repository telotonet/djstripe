from django.db import models
from django.urls import reverse


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_absolute_url(self):
        return reverse("get_item", args=[self.pk])


class Order(models.Model):
    items = models.ManyToManyField(Item)

    def get_absolute_url(self):
        return reverse("get_order", args=[self.pk])
