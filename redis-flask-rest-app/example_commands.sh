#!/bin/sh


redis-cli flushall

curl -i -H "Content-Type: application/json" -X POST -d '{"email": ["noel@hotmail.com"], "first_name": "Neil", "last_name":"Evans"}' http://localhost:5000/api/create/user:noel
curl -i -H "Content-Type: application/json" -X POST -d '{"email": ["kam@hotmail.com"], "first_name": "Cam", "last_name":"Evans"}' http://localhost:5000/api/create/user:kam

curl -i -H "Content-Type: application/json" -X PUT -d '{"email": "noel@gmail.com", "first_name": "Noel"}' http://localhost:5000/api/update/user:noel
curl -i -H "Content-Type: application/json" -X PUT -d '{"email": "kam@gmail.com", "first_name": "Kam"}' http://localhost:5000/api/update/user:kam

# curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/api/delete/user:noel

