#!/usr/bin/env python
# coding=UTF-8

import geoserverapirest.ext.postgis as pg
reload(pg)

pgi = pg.GsPostGis("db", "5432", "test_geoserver", "postgres", "postgres")

print pgi.getColumnData("data", "municipio", "area", sort=True, distinct=True)
