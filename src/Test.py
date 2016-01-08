#!/usr/bin/env python
# coding=UTF-8

import geoserverapirest.ext.postgis as pg, geoserverapirest.core as gs
import requests, json
reload(pg)
reload(gs)

i = pg.GsPostGis("db", "5432", "test_geoserver", "postgres", "postgres")

sql = """select * from data.municipio where "PROVINCIA"='Sevilla'"""

gsis = gs.GsInstance("http://sourcegeoserver:8080/geoserver")

ft = gsis.getFeatureType("new_workspace", "new_postgis_ds", "Sevilla")

ft["featureType"]["name"] = "Cordoba"
ft["featureType"]["metadata"]["entry"]["virtualTable"]["sql"] = \
    u'select * from data.municipio where "PROVINCIA"=\'Córdoba\'\n'

r = requests.post("http://sourcegeoserver:8080/geoserver/rest/workspaces/new_workspace/datastores/new_postgis_ds/featuretypes.json", 
        auth=("admin", "geoserver"), \
        headers={"Content-Type": "text/json"}, \
        data=json.dumps(ft))


r = requests.get("http://sourcegeoserver:8080/geoserver/rest/layers.json",
        auth=("admin", "geoserver"))
