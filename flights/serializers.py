from rest_framework import serializers
from .models import Flight
from rest_framework.validators import UniqueValidator


class FlightSerializer(serializers.ModelSerializer):
    fare = serializers.DecimalField(
        max_digits=8, decimal_places=2, coerce_to_string=False
    )

    class Meta:
        model = Flight
        fields = [
            "id",
            "departure_location",
            "arrival_location",
            "fare",
            "departure_time",
            "arrival_time",
        ]
