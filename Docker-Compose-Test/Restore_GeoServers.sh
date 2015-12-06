#!/bin/bash

# This script rebuild the whole testing environment

docker-compose stop
docker rm dockercomposetest_destinationgeoserver_1
docker rm dockercomposetest_geoserver_1
docker-compose up -d
docker-compose logs
