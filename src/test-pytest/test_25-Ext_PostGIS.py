#!/usr/bin/env python
# coding=UTF-8

import geoserverapirest.ext.postgis as pg
reload(pg)

"""
Requires the Docker-Compose to be up.

THIS TESTS ARE MEANT TO BE RUN INSIDE THE PYTHON-TEST CONTAINER OF THE DOCKER COMPOSE.
"""

class TestExtPostGis:
    """
    ext PostGIS test suite.
    """
    
    def setup(self):
        self.pgi = pg.GsPostGis("db", "5432", "test_geoserver", \
                                "postgres", "postgres")
                           

    def test_getFields(self):
        r = self.pgi.getFields("data", "municipio")
        self.pgi.close()

        expected = \
          {u'attributes': {
            u'attribute': [
              {
                u'maxOccurs': 1,
                u'nillable': True,
                u'binding': u'java.lang.Integer',
                u'name': u'gid',
                u'minOccurs': 0},
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
                u'minOccurs': 0}]}}

        assert r["attributes"]["attribute"]==expected["attributes"]["attribute"]
