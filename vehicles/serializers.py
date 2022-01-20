from rest_framework import serializers

from .exceptions import CarException, ReviewException
from .models import Car, Review
from .services.car_existence_checker import CarExistenceChecker


class CarSerializer(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'avg_rating']

    @staticmethod
    def get_avg_rating(obj):
        if obj.average_rating:
            return round(obj.average_rating, 1)

    def create(self, validated_data):
        model = validated_data['model']
        make = validated_data['make']
        car_checker = CarExistenceChecker(car_make=make, car_model=model)
        if car_checker.car_exists:
            return super().create(
                {'make': car_checker.clean_car_make, 'model': car_checker.clean_car_model}
            )
        else:
            raise CarException()


class ReviewSerializer(serializers.ModelSerializer):
    car_id = serializers.IntegerField(source='car.id', required=True)

    class Meta:
        model = Review
        fields = ['car_id', 'rating']

    def create(self, validated_data):
        car = validated_data.get('car', None)
        if not car:
            return
        car_id = car.get('id', None)
        rating = validated_data.get('rating', None)
        car = Car.objects.filter(id=int(car_id))
        if car.exists():
            return Review.objects.create(car=car.first(), rating=int(rating))
        else:
            raise ReviewException()

    def validate(self, attrs):
        if not attrs.get('rating'):
            raise serializers.ValidationError(
                {
                    'rating': 'To pole nie może być puste.'
                }
            )
        return super().validate(attrs)


class PopularSerializer(serializers.ModelSerializer):
    rates_number = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'rates_number']

    @staticmethod
    def get_rates_number(obj):
        return obj.rates_number
