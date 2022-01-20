from rest_framework import status
from rest_framework.test import APITestCase

from vehicles.models import Car
from vehicles.tests.factories import CarFactory


class ReviewAPITestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.rate_url = '/api/v1/rate/'

    def test_add_rating(self):
        car = CarFactory(model='Golf', make='Volkswagen')

        self.assertTrue(
            Car.objects.filter(model='Golf', make='Volkswagen').exists()
        )

        response = self.client.post(
            path=self.rate_url,
            data={
                'car_id': car.id,
                'rating': 5,
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_avg_rating(self):
        car1 = CarFactory(model='Golf', make='Volkswagen')
        car2 = CarFactory(model='Passat', make='Volkswagen')

        self.assertTrue(
            Car.objects.filter(id=car1.id).exists()
        )
        self.assertTrue(
            Car.objects.filter(id=car2.id).exists()
        )

        self.client.post(
            path=self.rate_url,
            data={
                'car_id': car1.id,
                'rating': 5,
            },
            format='json',
        )
        self.client.post(
            path=self.rate_url,
            data={
                'car_id': car2.id,
                'rating': 4,
            },
            format='json',
        )
        self.client.post(
            path=self.rate_url,
            data={
                'car_id': car2.id,
                'rating': 5,
            },
            format='json',
        )
        self.assertEqual(car1.average_rating, 5.0)
        self.assertEqual(car2.average_rating, 4.5)

