#!/usr/bin/env python
# coding=UTF-8

import geoserverapirest.ext.postgis as pg
reload(pg)

i = pg.GsPostGis("db", "5432", "test_geoserver", "postgres", "postgres")

sql = """select * from data.municipio where "PROVINCIA"='Sevilla'"""

i.getFieldsFromSql(sql, "geom", "Polygon")
