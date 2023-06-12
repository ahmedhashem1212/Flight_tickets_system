from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from accounts.models import User
from flights.models import Flight
from flights.serializers import FlightSerializer


class FlightTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="testpassword",
            is_staff=True,
        )
        self.client.login(email="testuser@gmail.com", password="testpassword")
        self.flight_data = {
            "departure_location": "Location A",
            "arrival_location": "Location B",
            "fare": 100.0,
            "departure_time": "2023-06-10T10:00:00",
            "arrival_time": "2023-06-10T12:00:00",
        }
        self.flight = Flight.objects.create(**self.flight_data)

    def test_flight_list_authenticated(self):
        url = reverse("flight-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_flight_list_unauthenticated(self):
        self.client.logout()
        url = reverse("flight-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_flight_model(self):
        self.assertEqual(self.flight.departure_location, "Location A")
        self.assertEqual(self.flight.arrival_location, "Location B")
        self.assertEqual(self.flight.fare, 100.0)

    def test_flight_serializer(self):
        serializer = FlightSerializer(instance=self.flight)
        self.assertEqual(serializer.data["departure_location"], "Location A")
        self.assertEqual(serializer.data["arrival_location"], "Location B")
        self.assertEqual(serializer.data["fare"], 100.0)

    def test_get_flight(self):
        url = reverse("flight-detail", kwargs={"flight_id": self.flight.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.flight.id)
        self.assertEqual(
            response.data["departure_location"], self.flight.departure_location
        )
        self.assertEqual(
            response.data["arrival_location"], self.flight.arrival_location
        )
        self.assertEqual(response.data["fare"], self.flight.fare)
        self.assertEqual(
            response.data["departure_time"][:-1], self.flight.departure_time
        )
        self.assertEqual(response.data["arrival_time"][:-1], self.flight.arrival_time)

    def test_update_flight(self):
        url = reverse("flight-detail", kwargs={"flight_id": self.flight.id})
        data = {
            "departure_location": "New Departure",
            "arrival_location": "New Arrival",
            "fare": 200.0,
            "departure_time": "2023-06-10T12:00:00Z",
            "arrival_time": "2023-06-10T14:00:00Z",
        }
        response = self.client.put(
            url, data, format="json", content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.flight.refresh_from_db()
        self.assertEqual(self.flight.departure_location, "New Departure")
        self.assertEqual(self.flight.arrival_location, "New Arrival")
        self.assertEqual(self.flight.fare, 200.0)
        self.assertEqual(
            self.flight.departure_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "2023-06-10T12:00:00",
        )
        self.assertEqual(
            self.flight.arrival_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "2023-06-10T14:00:00",
        )

    def test_delete_flight(self):
        url = reverse("flight-detail", kwargs={"flight_id": self.flight.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Flight.objects.filter(id=self.flight.id).exists())
