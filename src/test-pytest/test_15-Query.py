#!/usr/bin/env python
# coding=UTF-8

# import unittest as t, time
import geoserverapirest.core as gs
reload(gs)

"""
Requires two GeoServers for testing. Check Docker-Compose.
"""

class TestQuery:
    """
    Object query tests.
    """

    def setup(self):
        self.gsi = gs.GsInstance("http://localhost:8084/geoserver", "admin", "geoserver")


    def test_queryStylesNames(self):
        r = self.gsi.getStyleNames()
        assert set(r)==set([u"point", u"line", u"polygon", u"raster", u"new_style"])


    def test_queryFeatureTypesNames(self):
        r = self.gsi.getFeatureTypesNames("new_workspace", "new_postgis_ds")
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

        # Erase encrypted password
        del r["dataStore"]["connectionParameters"]["entry"][1]
        
        assert r=={u'dataStore':
                     {u'connectionParameters':
                       {u'entry': [
                         {u'@key': u'port', u'$': u'5432'},
                         {u'@key': u'dbtype', u'$': u'postgis'},
                         {u'@key': u'host', u'$': u'db'},
                         {u'@key': u'encode functions', u'$': u'false'},
                         {u'@key': u'validate connections', u'$': u'false'},
                         {u'@key': u'Support on the fly geometry simplification', u'$': u'false'},
                         {u'@key': u'database', u'$': u'test_geoserver'},
                         {u'@key': u'namespace', u'$': u'http://new_workspace'},
                         {u'@key': u'schema', u'$': u'data'},
                         {u'@key': u'Test while idle', u'$': u'false'},
                         {u'@key': u'Loose bbox', u'$': u'false'},
                         {u'@key': u'Expose primary keys', u'$': u'false'},
                         {u'@key': u'create database', u'$': u'false'},
                         {u'@key': u'preparedStatements', u'$': u'false'},
                         {u'@key': u'Estimated extends', u'$': u'false'},
                         {u'@key': u'user', u'$': u'postgres'}]},
                       u'featureTypes': u'http://localhost:8084/geoserver/rest/workspaces/new_workspace/datastores/new_postgis_ds/featuretypes.json',
                       u'name': u'new_postgis_ds',
                       u'enabled': True,
                       u'workspace': {u'href': u'http://localhost:8084/geoserver/rest/workspaces/new_workspace.json', u'name': u'new_workspace'},
                       u'_default': False,
                       u'type': u'PostGIS'}}
        

    def test_queryGetFeatureType(self):
        r = self.gsi.getFeatureType("new_workspace", "new_postgis_ds", "municipio")

        pAnswer = \
        {u'featureType':
          {u'circularArcPresent': False,
           u'nativeBoundingBox': {
             u'minx': 100401.207748027,
             u'miny': 3977032.24536145,
             u'maxx': 621272.560611986,
             u'maxy': 4288702.72162018,
             u'crs': {
               u'$': u'EPSG:25830',
               u'@class': u'projected'}
             },
          u'nativeCRS': {
            u'$': u'PROJCS["ETRS89 / UTM zone 30N", \n  GEOGCS["ETRS89", \n    DATUM["European Terrestrial Reference System 1989", \n      SPHEROID["GRS 1980", 6378137.0, 298.257222101, AUTHORITY["EPSG","7019"]], \n      TOWGS84[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], \n      AUTHORITY["EPSG","6258"]], \n    PRIMEM["Greenwich", 0.0, AUTHORITY["EPSG","8901"]], \n    UNIT["degree", 0.017453292519943295], \n    AXIS["Geodetic longitude", EAST], \n    AXIS["Geodetic latitude", NORTH], \n    AUTHORITY["EPSG","4258"]], \n  PROJECTION["Transverse_Mercator", AUTHORITY["EPSG","9807"]], \n  PARAMETER["central_meridian", -3.0], \n  PARAMETER["latitude_of_origin", 0.0], \n  PARAMETER["scale_factor", 0.9996], \n  PARAMETER["false_easting", 500000.0], \n  PARAMETER["false_northing", 0.0], \n  UNIT["m", 1.0], \n  AXIS["Easting", EAST], \n  AXIS["Northing", NORTH], \n  AUTHORITY["EPSG","25830"]]',
            u'@class': u'projected'},
          u'name': u'municipio',
          u'title': u'municipio',
          u'latLonBoundingBox': {
            u'minx': -7.591550494742739,
            u'miny': 35.85606982620556,
            u'maxx': -1.604639014703357,
            u'maxy': 38.74696558381656,
            u'crs': u'GEOGCS["WGS84(DD)", \n  DATUM["WGS84", \n    SPHEROID["WGS84", 6378137.0, 298.257223563]], \n  PRIMEM["Greenwich", 0.0], \n  UNIT["degree", 0.017453292519943295], \n  AXIS["Geodetic longitude", EAST], \n  AXIS["Geodetic latitude", NORTH]]'
          },
          u'enabled': True,
          u'namespace': {
            u'href': u'http://localhost:8084/geoserver/rest/namespaces/new_workspace.json',
            u'name': u'new_workspace'
          },
          u'projectionPolicy': u'FORCE_DECLARED',
          u'numDecimals': 0,
          u'srs': u'EPSG:25830',
          u'keywords': {
            u'string': [u'municipio', u'features']
          },
          u'attributes': {
            u'attribute': [
              {
                u'maxOccurs': 1,
                u'nillable': True,
                u'binding': u'java.lang.String',
                u'name': u'COD_MUN',
                u'minOccurs': 0},
              {
                u'maxOccurs': 1,
                u'nillable': True,
                u'binding': u'java.lang.String',
                u'name': u'MUNICIPIO',
                u'minOccurs': 0},
              {
                u'maxOccurs': 1,
                u'nillable': True,
                u'binding': u'java.lang.String',
                u'name': u'PROVINCIA',
                u'minOccurs': 0},
              {
                u'maxOccurs': 1,
                u'nillable': True,
                u'binding': u'java.lang.String',
                u'name': u'COD_ENT',
                u'minOccurs': 0},
              {
                u'maxOccurs': 1,
                u'nillable': True,
                u'binding': u'com.vividsolutions.jts.geom.MultiPolygon',
                u'name': u'geom',
                u'minOccurs': 0}]},
          u'nativeName': u'municipio',
          u'maxFeatures': 0,
          u'store': {
            u'href': u'http://localhost:8084/geoserver/rest/workspaces/new_workspace/datastores/new_postgis_ds.json',
            u'name': u'new_postgis_ds',
            u'@class': u'dataStore'},
          u'overridingServiceSRS': False}}

        assert r==pAnswer




        

