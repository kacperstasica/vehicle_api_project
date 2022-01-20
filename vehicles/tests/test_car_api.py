from unittest.mock import patch

from rest_framework import status
from rest_framework.test import APITestCase

from ..exceptions import CarException
from ..models import Car
from .factories import CarFactory


class CarApiTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cars_url = '/cars/'

    @patch('vehicles.services.car_existence_checker.CarExistenceChecker.get_vehicles_response')
    def test_car_create(self, mock_response):
        mock_response.return_value = [
            {
                'Make_ID': 482,
                'Make_Name': 'Foo',
                'Model_ID': 1951,
                'Model_Name': 'Bar'
            }
        ]
        self.assertFalse(
            Car.objects.filter(model='Foo', make='Bar').exists()
        )
        response = self.client.post(
            path=self.cars_url,
            data={
                'make': 'Foo',
                'model': 'Bar',
            },
            format='json',
        )

        self.assertTrue(
            Car.objects.filter(model='Bar', make='Foo').exists()
        )
        self.assertEqual(response.status_code, 201)

    @patch('vehicles.services.car_existence_checker.CarExistenceChecker.get_vehicles_response')
    def test_create_car_that_does_not_exist(self, mock_response):
        mock_response.return_value = None
        self.assertFalse(
            Car.objects.filter(model='Foo', make='Bar').exists()
        )
        response = self.client.post(
                path=self.cars_url,
                data={
                    'make': 'Foo',
                    'model': 'Bar',
                },
                format='json',
            )
        self.assertEqual(
            response.status_code,
            status.HTTP_503_SERVICE_UNAVAILABLE
        )

        self.assertEqual(
            response.json().get('detail'),
            CarException.default_detail
        )

    @patch('vehicles.services.car_existence_checker.CarExistenceChecker.get_vehicles_response')
    def test_car_create_with_upper_model_name(self, mock_response):
        mock_response.return_value = [
            {
                'Make_ID': 482,
                'Make_Name': 'Foo',
                'Model_ID': 1951,
                'Model_Name': 'Bar'
            }
        ]
        self.assertFalse(
            Car.objects.filter(model='Foo', make='Bar').exists()
        )
        response = self.client.post(
            path=self.cars_url,
            data={
                'make': 'FoO',
                'model': 'BAr',
            },
            format='json',
        )

        self.assertTrue(
            Car.objects.filter(model='Bar', make='Foo').exists()
        )
        self.assertEqual(response.status_code, 201)

    def test_car_delete(self):
        car = CarFactory(model='Golf', make='Volkswagen')

        self.assertTrue(
            Car.objects.filter(model='Golf', make='Volkswagen').exists()
        )
        self.client.delete(
            path=f'{self.cars_url}{car.id}/'
        )
        self.assertFalse(
            Car.objects.filter(model='Golf', make='Volkswagen').exists()
        )

    def test_delete_car_that_does_not_exist(self):
        car = CarFactory(model='Foo', make='Bar')
        self.assertTrue(
            Car.objects.filter(id=car.id).exists()
        )

        self.client.delete(path=f'{self.cars_url}{car.id}/')
        response = self.client.delete(
            path=f'{self.cars_url}{car.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
        self.assertFalse(
            Car.objects.filter(id=car.id).exists()
        )
