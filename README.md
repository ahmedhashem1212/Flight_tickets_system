# Flight_tickets_system
* The system provides a facility to search for the available flights between two
locations. As well, demonstrating fare, departure and arrival times of the different
flights. It allows user to make a reservation of flight and upgrading the ticket class.

* If you wanna run the server use this command:
    python manage.py runserver

* MySQL database is used here and configured in config.yml.

* Authentication used here is JWT

* I cover the api with number of sutible unit test cases if you wanna run the test cases use this command:
    python manage.py test
    
* Here we have 3 implemented apps I am gonna talk deeply about each one of them.
----------------------
1-Accounts
---------------------
* it is an application that defines the user and admin models. I develop this app for authentication and authorization step to generate a token for both user or admin when i login. I implement two apis here. 

1- http://127.0.0.1:8000/users/signup/  (post)

--Request_to_create_admin--->                   --Request_to_create_user--->             
{                                              {   
   "username":"user",                             "username":"user",
   "email":"user5@gmail.com",                     "email":"user5@gmail.com",
   "password":"user1234",                         "password":"user1234",
   "is_staff":true                                "is_staff":false
}                                              }

----response ---->
{
    "message": "User Created Successfully",
    "data": {
        "email": "user@gmail.com",
        "username": "user",
        "is_staff": true
    }
}

2- http://127.0.0.1:8000/users/login/   (post)

--Request_to_create_admin--->               
{   
    "email":"user5@gmail.com",
    "password":"user1234",
 }

----response ---->
{
    "message": "Login Successfull",
    "token": {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg2NTQzOTY2LCJpYXQiOjE2ODY1NDAzNjYsImp0aSI6ImQzNjkxOWViYTkxYzQ1Y2Y5YjYxZDIxMGYzZDJmNmQwIiwidXNlcl9pZCI6Nn0.WHXqql-F4vOjjSt4yBgMwMcSsY_GAZC8z4miLzFXTzA"
    }
}
* I used the access token to access different api (embed the token in the headers of each api)

-------------------------------------------------------
2- Flights
----------------
* The app to define a flight model in the DB and its related apis. The model has 5 attributes:
    id (primary key)
    departure_location 
    arrival_location 
    fare 
    departure_time 
    arrival_time 
    we implement here 6 apis as follows:

1- http://127.0.0.1:8000/flights/   (admin token should be in the header) (get)

--request---> {}

--response --> with status 200  [
    {
        "id": 3,
        "departure_location": "Cairo",
        "arrival_location": "Paris",
        "fare": 10.0,
        "departure_time": "2023-04-14T21:23:49Z",
        "arrival_time": "2023-04-14T21:23:49Z"
    },
    {
        "id": 4,
        "departure_location": "Cairo",
        "arrival_location": "Paris",
        "fare": 2000.0,
        "departure_time": "2023-04-14T21:23:49Z",
        "arrival_time": "2023-04-14T21:23:49Z"
    }
    ]

2- http://127.0.0.1:8000/flights/:id  (admin token should be in the header) (get)

--request--->{}
--response--->
{
    "id": 1,
    "departure_location": "Cairo",
    "arrival_location": "Paris",
    "fare": "50.00",
    "departure_time": "2023-04-14T21:23:49Z",
    "arrival_time": "2023-04-14T21:23:49Z"
}

3- http://127.0.0.1:8000/flights/ (admin token should be in the header) (post)

--request ---> 
{
        "departure_location": "Cairo",
        "arrival_location": "Paris",
        "fare": "50.00",
        "departure_time": "2023-04-14T21:23:49Z",
        "arrival_time": "2023-04-14T21:23:49Z"
}
--response--->
{
    "id": 4,
    "departure_location": "Cairo",
    "arrival_location": "Paris",
    "fare": "50.00",
    "departure_time": "2023-04-14T21:23:49Z",
    "arrival_time": "2023-04-14T21:23:49Z"
}

4- http://127.0.0.1:8000/flights/:id (admin token should be in the header) (post)

--request ---> 
{
        "departure_location": "Cairo",
        "arrival_location": "Paris",
        "fare": "50.00",
        "departure_time": "2023-04-14T21:23:49Z",
        "arrival_time": "2023-04-14T21:23:49Z"
}
--response---> status 201 created
{
    "id": 4,
    "departure_location": "Cairo",
    "arrival_location": "Paris",
    "fare": "50.00",
    "departure_time": "2023-04-14T21:23:49Z",
    "arrival_time": "2023-04-14T21:23:49Z"
}

5- http://127.0.0.1:8000/flights/:id (admin token should be in the header) (delete)

--request ---> {}
--response---> status 204 no content{}

6- http://127.0.0.1:8000/flights/search/?from=%&to=%&fare_min=%&fare_max=% 
(user token should be in the header) (get)

--request --->{}
--response --->
[
    {
        "id": 4,
        "departure_location": "Cairo",
        "arrival_location": "Paris",
        "fare": 2000.0,
        "departure_time": "2023-04-14T21:23:49Z",
        "arrival_time": "2023-04-14T21:23:49Z"
    }
]

** User can search on the flights using to and from and the range of price (optional) (fare_max or fare_min or both of them or none of them) 

---------------------------------------- 
3- Bookings
---------
** The app to define a booking model in the DB and its related apis. The model has 5 attributes:
    id (primary key)
    flight (forign key to the flight model)
    user (forign key to the account model)
    ticket_class (enum has 4 options  economy,premium_economy,business,first_class) 
    price 
    we implement here 3 apis as follows:

1- http://127.0.0.1:8000/bookings/  (user token should be in the header) (post)

--Request--->
{   
    "flight":4,
    "user":1,
    "ticket_class":"economy",
    "price":100
}

--Response ---> 201 created
{
    "id": 7,
    "ticket_class": "economy",
    "price": "100.00",
    "flight": 4,
    "user": 1
}

2- http://127.0.0.1:8000/bookings/upgrade/:id (user token should be in the header) (put)

--Request --->
{   
    "ticket_class":"premium_economy",
    "price":150 
}

--Response---> {
    "id": 7,
    "ticket_class": "premium_economy",
    "price": "150.00",
    "flight": 4,
    "user": 1
}

3- http://127.0.0.1:8000/bookings/cancel/7  (user token should be in the header) (delete)

--Request ---> {}
--Response ---> 204 no content
{}









