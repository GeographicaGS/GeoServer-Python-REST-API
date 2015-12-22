Objectives
==========

This is an ongoing project for creating a Python REST API module for interacting with GeoServer. It is by no means complete, it's just a tool for automating certain admin tasks here at Geographica, like for example harvesting info about layers and its databases of origin. There is no intention to create a full-fledged module with all the functionality provided by the API, just what we are needing on the fly.

Development Environment
=======================

A Docker Compose deployment is used for testing, consisting in two GeoServers, a PostGIS DB and a Python development environment. To initialize it, just:

```Shell
./Restore_GeoServers.sh
```

will create everything needed. Then the usual Docker Compose commands can be used to start and stop the cluster.

The only configuration needed is to the __python-dev__ container, that is hard-mounting the code folder as a volume. Check _volumes_ in __docker-compose.yml__, _python-dev_ section to change to your code base folder.

Once the Docker cluster is created, just enter into the _python-dev_ container with:

```Shell
docker exec -ti geoserverapirestdockercompose_python-dev_1 /bin/bash
```

to test code with __py.test__:

```Shell
py.test -vv
```

Changelog
=========

Version 0.1:

- Basic information reading for a GeoServer instances, layers, workspaces, data stores, and feature types, just for basic harvesting and cataloging, with a special emphasis on PostGIS data stores with the aim to trace back the origin of data sources from layers to database.

TODO
====

- Document current version (v0.1).

- Make the API more coherent between objects, revise terminology.

Known Issues and Caveats
========================

