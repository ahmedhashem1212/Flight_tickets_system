from django.db import models
from django.core.exceptions import ValidationError


class Flight(models.Model):
    departure_location = models.CharField(max_length=100)
    arrival_location = models.CharField(max_length=100)
    fare = models.DecimalField(max_digits=8, decimal_places=2)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def clean(self):
        if self.departure_location == self.arrival_location:
            raise ValidationError("Departure and arrival locations cannot be the same.")

        if self.fare < 0:
            raise ValidationError("Fare must be a non-negative value.")

        if self.departure_time >= self.arrival_time:
            raise ValidationError(
                "Departure time must be earlier than the arrival time."
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Flight from {self.departure_location} to {self.arrival_location}"
