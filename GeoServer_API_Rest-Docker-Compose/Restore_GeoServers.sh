#!/bin/bash

# This script rebuild the whole testing environment

docker-compose stop
docker rm -v dockercomposetest_destinationgeoserver_1
docker rm -v dockercomposetest_sourcegeoserver_1
docker-compose up -d
docker-compose logs
