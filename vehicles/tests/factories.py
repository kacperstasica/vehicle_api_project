import factory

from vehicles.models import Car


class CarFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Car
