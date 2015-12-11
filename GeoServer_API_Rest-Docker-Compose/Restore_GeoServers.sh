#!/bin/bash

# This script rebuild the whole testing environment

docker-compose stop
docker-compose rm -v -f
docker-compose up -d

echo Waiting 23s for the PostgreSQL container to be up...
sleep 23s

# Repopulate database
PGPASSWORD="postgres" psql -h localhost -p 5435 -U postgres postgres -f DB-Test/00-Database-DDL.sql
PGPASSWORD="postgres" psql -h localhost -p 5435 -U postgres test_geoserver -f DB-Test/10-Data-Municipio-DDL.sql
PGPASSWORD="postgres" psql -h localhost -p 5435 -U postgres postgres -f DB-Test/20-Database-Postprocessing.sql
