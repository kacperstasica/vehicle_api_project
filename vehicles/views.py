from django.db.models import Avg, Count
from rest_framework import viewsets, mixins

from .models import Car, Review
from .serializers import CarSerializer, ReviewSerializer, PopularSerializer


class CarViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    serializer_class = CarSerializer

    def get_queryset(self):
        return Car.objects.all().annotate(avg_rating=Avg('review__rating'))


class ReviewViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class PopularViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PopularSerializer

    def get_queryset(self):
        return Car.objects.all().annotate(number_of_rates=Count('review')).order_by('-number_of_rates')
