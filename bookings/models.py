from django.db import models

# from django.contrib.auth.models import User
from accounts.models import User
from flights.models import Flight
from django.core.validators import MinValueValidator, ValidationError


class Booking(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    TICKET_CLASS_CHOICES = [
        ("economy", "Economy"),
        ("premium_economy", "Premium Economy"),
        ("business", "Business"),
        ("first_class", "First Class"),
    ]

    ticket_class = models.CharField(max_length=15, choices=TICKET_CLASS_CHOICES)
    price = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(0)], default=0
    )

    def clean(self):
        if self.price < 0:
            raise ValidationError("Price must be a non-negative value.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking: {self.flight} - {self.user}"
