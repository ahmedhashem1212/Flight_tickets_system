from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    ticket_class = serializers.ChoiceField(
        choices=Booking.TICKET_CLASS_CHOICES, required=True
    )

    class Meta:
        model = Booking
        fields = "__all__"
