from django.db import models
from django.db.models import Avg, Count


class Car(models.Model):
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Samochód'
        verbose_name_plural = 'Samochody'

    def __str__(self):
        return f'Make: {self.make} Model: {self.model}'

    @property
    def average_rating(self):
        if hasattr(self, 'avg_rating'):
            return self.avg_rating
        return self.review_set.aggregate(Avg('rating')).get('rating__avg', None)

    @property
    def rates_number(self):
        if hasattr(self, 'number_of_rates'):
            return self.number_of_rates
        return self.review_set.aggregate(Count('rating'))


class Review(models.Model):
    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(null=True, blank=False, choices=RATING_CHOICES)

    class Meta:
        verbose_name = 'Ocena'
        verbose_name_plural = 'Oceny'

    def __str__(self):
        return f'Car: {self.car} Rating: {self.rating}'
