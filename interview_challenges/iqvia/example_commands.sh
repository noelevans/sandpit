#!/bin/sh


# rm -f contact_manager.db

curl -i -H "Content-Type: application/json" -X POST -d '{"username": "noel", "first_name": "Neil", "last_name":"Evans"}' http://localhost:5000/api/create/contact
curl -i -H "Content-Type: application/json" -X POST -d '{"username": "kam", "first_name": "Cam", "last_name":"Ifans"}' http://localhost:5000/api/create/contact
curl -i -H "Content-Type: application/json" -X POST -d '{"username": "kam", "address": "kam@gmail.com"}' http://localhost:5000/api/create/email

curl -i -H "Content-Type: application/json" -X PUT -d '{"first_name": "Noel"}' http://localhost:5000/api/update/contact/noel
curl -i -H "Content-Type: application/json" -X PUT -d '{"first_name": "Kam", "last_name": "Evans"}' http://localhost:5000/api/update/contact/kam

curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/api/delete/contact/noel

