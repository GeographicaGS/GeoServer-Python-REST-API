#!/usr/bin/env python
# coding=UTF-8

import geoserverapirest.core as gs, geoserverapirest.ext.const as const
reload(gs)

"""
Requires two GeoServers for testing. Check Docker-Compose.

THIS TESTS ARE MEANT TO BE RUN INSIDE THE PYTHON-TEST CONTAINER OF THE DOCKER COMPOSE.

TODO: change name to some test to the name of the function being tested.

TODO: clean a GeoServer and do tests on an empty on.
"""

class TestQuery:
    """
    Object query tests.
    """

    def setup(self):
        self.gsi = gs.GsInstance("http://sourcegeoserver:8080/geoserver", "admin", "geoserver")


    def test_queryStylesNames(self):
        r = self.gsi.getStyleNames()
        assert set(r)==set([u"point", u"line", u"polygon", u"raster", u"new_style"])


    def test_queryFeatureTypeNames(self):
        r = self.gsi.getFeatureTypeNames("new_workspace", "new_postgis_ds")
        assert set(r)==set([u"municipio"])


    def test_queryDataStoresNames(self):
        r = self.gsi.getDataStoreNames("new_workspace")
        assert set(r)==set([u"new_postgis_ds"])


    def test_queryNamespacesNames(self):
        r = self.gsi.getNamespaceNames()
        assert set(r)==set([u"new_workspace"])

        
    def test_queryWorkspacesNames(self):
        r = self.gsi.getWorkspaceNames()
        assert set(r)==set([u"new_workspace"])


    def test_queryGetDataStore(self):
        r = self.gsi.getDataStore("new_workspace", "new_postgis_ds")

        assert isinstance(r, dict)
        assert u"dataStore" in r.keys()
        
        r = r[u"dataStore"]
        assert isinstance(r, dict)
        
        for i in [u"connectionParameters", u"featureTypes", u"name", \
                  u"enabled", u"workspace", u"_default", u"type"]:
            assert i in r.keys()
            
        assert r["featureTypes"]==u'http://sourcegeoserver:8080/geoserver/rest/workspaces/new_workspace/datastores/new_postgis_ds/featuretypes.json'
        assert r["name"]==u'new_postgis_ds'
        assert r["enabled"]==True
        assert r["workspace"]=={u'href': u'http://sourcegeoserver:8080/geoserver/rest/workspaces/new_workspace.json', u'name': u'new_workspace'}
        assert r["_default"]==False
        assert r["type"]==u'PostGIS'

        r = r["connectionParameters"]
        assert isinstance(r, dict)
        assert "entry" in r.keys()

        r = r["entry"]
        assert isinstance(r, list)
        assert {u'@key': u'port', u'$': u'5432'} in r
        assert {u'@key': u'dbtype', u'$': u'postgis'} in r
        assert {u'@key': u'host', u'$': u'db'} in r
        assert {u'@key': u'encode functions', u'$': u'false'} in r
        assert {u'@key': u'validate connections', u'$': u'false'} in r
        assert {u'@key': u'Support on the fly geometry simplification', u'$': u'false'} in r
        assert {u'@key': u'database', u'$': u'test_geoserver'} in r
        assert {u'@key': u'namespace', u'$': u'http://new_workspace'} in r
        assert {u'@key': u'schema', u'$': u'data'} in r
        assert {u'@key': u'Test while idle', u'$': u'false'} in r
        assert {u'@key': u'Loose bbox', u'$': u'false'} in r
        assert {u'@key': u'Expose primary keys', u'$': u'true'} in r
        assert {u'@key': u'create database', u'$': u'false'} in r
        assert {u'@key': u'preparedStatements', u'$': u'false'} in r
        assert {u'@key': u'Estimated extends', u'$': u'false'} in r
        assert {u'@key': u'user', u'$': u'postgres'} in r


    def test_getConnDataFromPostGisDataStore(self):
        r = self.gsi.getConnDataFromPostGisDataStore("new_workspace", "new_postgis_ds")

        expected = \
          {"port": "5432",
           "host": "db",
           "database": "test_geoserver",
           "schema": "data",
           "user": "postgres"}
           
        assert r==expected
                

    def test_queryGetFeatureType(self):
        r = self.gsi.getFeatureType("new_workspace", "new_postgis_ds", "municipio")

        assert isinstance(r, dict)
        assert u"featureType" in r.keys()

        r = r["featureType"]
        assert isinstance(r, dict)

        for i in [u'circularArcPresent', u'nativeBoundingBox', u'nativeCRS', u'name', u'title', u'latLonBoundingBox', u'enabled', u'namespace', u'projectionPolicy', u'numDecimals', u'srs', u'keywords', u'attributes', u'nativeName', u'maxFeatures', u'store', u'overridingServiceSRS']:
            assert i in r.keys()

        assert r["circularArcPresent"]==False
        
        assert r["nativeBoundingBox"]=={
            u'minx': 100401.207748027,
            u'miny': 3977032.24536145,
            u'maxx': 621272.560611986,
            u'maxy': 4288702.72162018,
            u'crs': {
                u'$': u'EPSG:25830',
                u'@class': u'projected'}
            }
        
        assert r["nativeCRS"]["@class"]==u"projected"
        assert r["name"]==u'municipio'
        assert r["title"]==u'Municipios de Andalucía'
                
        assert r[u'latLonBoundingBox']=={
            u'minx': -7.591550494742739,
            u'miny': 35.85606982620556,
            u'maxx': -1.604639014703357,
            u'maxy': 38.74696558381656,
            u'crs': u'GEOGCS["WGS84(DD)", \n  DATUM["WGS84", \n    SPHEROID["WGS84", 6378137.0, 298.257223563]], \n  PRIMEM["Greenwich", 0.0], \n  UNIT["degree", 0.017453292519943295], \n  AXIS["Geodetic longitude", EAST], \n  AXIS["Geodetic latitude", NORTH]]'}
        
        assert r[u'enabled']==True
        
        assert r[u'namespace']=={
            u'href': u'http://sourcegeoserver:8080/geoserver/rest/namespaces/new_workspace.json',
            u'name': u'new_workspace'}
        
        assert r[u'projectionPolicy']==u'FORCE_DECLARED'
        assert r[u'numDecimals']==0
        assert r[u'srs']==u'EPSG:25830'
        assert r[u'nativeName']==u'municipio'
        assert r[u'maxFeatures']==0
        
        assert r[u'store']=={
            u'href': u'http://sourcegeoserver:8080/geoserver/rest/workspaces/new_workspace/datastores/new_postgis_ds.json',
            u'name': u'new_postgis_ds',
            u'@class': u'dataStore'}
        
        assert r[u'overridingServiceSRS']==False

        for i in [u'municipio', u'features']:
            assert i in r["keywords"]["string"]

        assert isinstance(r["attributes"]["attribute"], list)
        
        for i in [{u'maxOccurs': 1, u'nillable': True, u'binding': u'java.lang.Integer', u'name': u'gid', u'minOccurs': 0}, {u'maxOccurs': 1, u'nillable': True, u'binding': u'java.lang.String', u'name': u'COD_MUN', u'minOccurs': 0}, {u'maxOccurs': 1, u'nillable': True, u'binding': u'java.lang.String', u'name': u'MUNICIPIO', u'minOccurs': 0}, {u'maxOccurs': 1, u'nillable': True, u'binding': u'java.lang.String', u'name': u'PROVINCIA', u'minOccurs': 0}, {u'maxOccurs': 1, u'nillable': True, u'binding': u'java.lang.String', u'name': u'COD_ENT', u'minOccurs': 0}, {u'maxOccurs': 1, u'nillable': True, u'binding': u'com.vividsolutions.jts.geom.MultiPolygon', u'name': u'geom', u'minOccurs': 0}]:
            assert i in r["attributes"]["attribute"]


    def test_getLayerNames(self):
        r = self.gsi.getLayerNames()
        assert r==["municipio"]


    def test_getLayer(self):
        r = self.gsi.getLayer("municipio")

        assert isinstance(r, dict)
        assert "layer" in r.keys()

        r = r["layer"]

        assert set(r.keys())== \
          set([u'styles', u'resource', u'name', u'opaque', u'defaultStyle', \
               u'attribution', u'type', u'queryable'])

        assert r["attribution"]=={"logoWidth":0,"logoHeight":0}

        assert r["defaultStyle"]== \
          {u'href': u'http://sourcegeoserver:8080/geoserver/rest/styles/polygon.json', u'name': u'polygon'}

        assert r["resource"]== \
          {u'href': u'http://sourcegeoserver:8080/geoserver/rest/workspaces/new_workspace/datastores/new_postgis_ds/featuretypes/municipio.json', u'name': u'municipio', u'@class': u'featureType'}

        r = r["styles"]["style"]

        for i in [{u'href': u'http://sourcegeoserver:8080/geoserver/rest/styles/polygon.json', u'name': u'polygon'}, {u'href': u'http://sourcegeoserver:8080/geoserver/rest/styles/line.json', u'name': u'line'}, {u'href': u'http://sourcegeoserver:8080/geoserver/rest/styles/point.json', u'name': u'point'}]:
            assert i in r
