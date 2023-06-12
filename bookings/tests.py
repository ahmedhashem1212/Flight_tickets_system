from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from flights.models import Flight
from accounts.models import User
from bookings.models import Booking


class BookingTestCase(TestCase):
    def setUp(self):
        self.flight = Flight.objects.create(
            departure_location="City A",
            arrival_location="City B",
            fare=100,
            departure_time="2023-06-10T10:00:00Z",
            arrival_time="2023-06-10T12:00:00Z",
        )
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="testpassword",
            is_staff=False,
        )
        self.client.login(email="testuser@gmail.com", password="testpassword")
        self.booking = Booking.objects.create(
            flight=self.flight,
            user=self.user,
            ticket_class="economy",
            price=100,
        )

    def test_book_flight(self):
        url = reverse("book-flight")
        data = {
            "flight": self.flight.id,
            "user": self.user.id,
            "ticket_class": "economy",
            "price": 150,
        }
        response = self.client.post(
            url, data, format="json", content_type="application/json"
        )
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        booking = Booking.objects.get(id=response.data["id"])
        self.assertEqual(booking.flight, self.flight)
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.ticket_class, "economy")
        self.assertEqual(booking.price, 150)

    def test_upgrade_ticket(self):
        url = reverse("upgrade-booking", kwargs={"booking_id": self.booking.id})
        data = {"ticket_class": "business", "price": 100}
        response = self.client.put(
            url, data, format="json", content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.ticket_class, "business")
        self.assertEqual(self.booking.price, 100)

    def test_cancel_booking(self):
        url = reverse("cancel-booking", kwargs={"booking_id": self.booking.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Booking.objects.filter(id=self.booking.id).exists())
