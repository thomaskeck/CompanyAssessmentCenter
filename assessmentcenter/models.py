from django.db import models
from django.utils import timezone

# Create your models here.

class Benchmark(models.Model):
    name = models.CharField(max_length=100)
    weight = models.FloatField(default=1.0)
    
    def __str__(self):
        return self.name


class Offer(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=10000)
    deadline = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name

    def is_expired(self):
        return self.deadline is not None and self.deadline < timezone.now()


class Rating(models.Model):
    benchmark = models.ForeignKey(Benchmark, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.rating)
