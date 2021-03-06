# Virtual Store API

## Introduction

This application aims to simulate a virtual store back-end. It was developed on Python 3.8, Django, and Django Rest Framework.

This project is under development at this moment. It intends to give digital sales capability to some retail. There is a need to develop a customer and product CRUD, and an order feature.

To do so, this project will have the following classes:
- Customer
- Person(Customer)
- Company(Customer)
- Product
- Order
- OrderItem

## Instalation process

This project was created over Docker infrastructure. The installation process has the following steps:

### 1. Project cloning

git clone https://github.com/evtlucas/virtual_store_api_test.git

### 2. Docker

The process of building and running the project's docker container has the following steps:

```
sudo docker-compose build
sudo docker-compose up
```

It is necessary to run the following commands after the container is up.

```
sudo docker-compose exec web sh
python manage.py migrate
python manage.py createsuperuser
```

It is possible to test whether the program is running by typing `http://localhost:8000/people/` on the browser. You'll see the Django Rest Framework's screen.

## Documentation

The API documentation could be acessed through http://localhost:8000/swagger/
