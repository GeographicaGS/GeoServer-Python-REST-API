#!/usr/bin/env python
# coding=UTF-8

import geoserverapirest.ext.postgis as pg, geoserverapirest.core as gs
reload(pg)
reload(gs)

i = pg.GsPostGis("db", "5432", "test_geoserver", "postgres", "postgres")

sql = """select * from data.municipio where "PROVINCIA"='Sevilla'"""

i.getFieldsFromSql(sql, "geom", "Polygon")

gsid = gs.GsInstance("http://destinationgeoserver:8080/geoserver")

gsis = gs.GsInstance("http://sourcegeoserver:8080/geoserver")

print gsis.getFeatureType("new_workspace", "new_postgis_ds", "municipios_sevilla")

