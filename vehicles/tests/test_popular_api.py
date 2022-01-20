from rest_framework.test import APITestCase

from .factories import CarFactory


class PopularAPITestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.popular_url = '/popular/'
        cls.rate_url = '/rate/'
        cls.car1 = CarFactory(model='Golf', make='Volkswagen')
        cls.car2 = CarFactory(model='Passat', make='Volkswagen')
        cls.car3 = CarFactory(model='DB9', make='ASTON MARTIN')
        cls.car4 = CarFactory(model='Civic', make='Honda')
        cls.car5 = CarFactory(model='Astra', make='OPEL')

    def setUp(self):
        for i in range(3):
            self.rate_car(self.car1, 4)
        for i in range(4):
            self.rate_car(self.car2, 3)
        for i in range(5):
            self.rate_car(self.car3, 5)
        for i in range(6):
            self.rate_car(self.car4, 2)
        for i in range(10):
            self.rate_car(self.car5, 5)

    def rate_car(self, car, rating):
        self.client.post(
            path=self.rate_url,
            data={
                'car_id': car.id,
                'rating': rating,
            },
            format='json',
        )

    def test_ordering_by_rates_number(self):
        response = self.client.get(self.popular_url)

        self.assertEqual(
            [element['id'] for element in response.json()],
            [self.car5.id, self.car4.id, self.car3.id, self.car2.id, self.car1.id]
        )
