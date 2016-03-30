#!/usr/bin/env python
# coding=UTF-8

import geoserverapirest.ext.postgis.core as pg
import test_data as td
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
        self.pgi = pg.GsPostGis({"host": "db", "port": "5432", "db": "test_geoserver", \
                                 "user": "postgres", "pass": "postgres"})

            
    def test_getFieldsFromTable(self):
        """
        Test getFieldsFromTable.
        """

        r = self.pgi.getFieldsFromTable("data", "municipio", "geom")
        self.pgi.close()
       
        assert isinstance(r, dict)
        assert "attributes" in r.keys()

        r = r["attributes"]
        assert isinstance(r, dict)
        assert "attribute" in r.keys()

        r = r["attribute"]

        for i in [{u'maxOccurs': 1, u'nillable': True, u'binding': u'java.lang.Integer',
                   u'name': 'gid', u'minOccurs': 0},
                  {u'maxOccurs': 1, u'nillable': True, u'binding': u'java.lang.String',
                   u'name': 'COD_MUN', u'minOccurs': 0},
                  {u'maxOccurs': 1, u'nillable': True, u'binding': u'java.lang.String',
                   u'name': 'MUNICIPIO', u'minOccurs': 0},
                  {u'maxOccurs': 1, u'nillable': True, u'binding': u'java.lang.String',
                   u'name': 'PROVINCIA', u'minOccurs': 0},
                  {u'maxOccurs': 1, u'nillable': True, u'binding': u'java.lang.String',
                   u'name': 'COD_ENT', u'minOccurs': 0},
                  {u'maxOccurs': 1, u'nillable': True, u'binding':
                   u'com.vividsolutions.jts.geom.MultiPolygon', u'name': 'geom', u'minOccurs': 0}]:
            assert i in r


    def test_getFieldsFromSql(self):
        """
        Test getFieldsFromTable.
        """

        r = self.pgi.getFieldsFromSql("select * from data.municipio", "geom")
        self.pgi.close()

        assert isinstance(r, dict)
        assert "attributes" in r.keys()

        r = r["attributes"]
        assert isinstance(r, dict)
        assert "attribute" in r.keys()

        r = r["attribute"]

        for i in [{u'maxOccurs': 1, u'nillable': True, u'binding': u'java.lang.Integer',
                   u'name': 'gid', u'minOccurs': 0},
                  {u'maxOccurs': 1, u'nillable': True, u'binding': u'java.lang.String',
                   u'name': 'COD_MUN', u'minOccurs': 0},
                  {u'maxOccurs': 1, u'nillable': True, u'binding': u'java.lang.String',
                   u'name': 'MUNICIPIO', u'minOccurs': 0},
                  {u'maxOccurs': 1, u'nillable': True, u'binding': u'java.lang.String',
                   u'name': 'PROVINCIA', u'minOccurs': 0},
                  {u'maxOccurs': 1, u'nillable': True, u'binding': u'java.lang.String',
                   u'name': 'COD_ENT', u'minOccurs': 0},
                  {u'maxOccurs': 1, u'nillable': True, u'binding':
                   u'com.vividsolutions.jts.geom.MultiPolygon', u'name': 'geom', u'minOccurs': 0}]:
            assert i in r


    def test_getColumnMinMax(self):
        """
        Test getColumnMinMax.
        """

        r = self.pgi.getColumnMinMax("data", "municipio", "area")
        self.pgi.close()
        assert r == [1647885.88, 1254911103.14]


    def test_getColumnDataFromTable(self):
        """
        Test getColumnDataFromTable.
        """

        rAll = self.pgi.getColumnDataFromTable("data", "municipio", "area")
        rSorted = self.pgi.getColumnDataFromTable("data", "municipio", "area", sort=True)
        rSortedReverse = self.pgi.getColumnDataFromTable("data", "municipio", "area", sort=True, \
                                                         reverse=True)
        rDistinctSorted = self.pgi.getColumnDataFromTable("data", "municipio", "area", sort=True, \
                                                          distinct=True)
        self.pgi.close()

        assert rAll == td.rAll

        assert rSorted == td.rSorted

        assert rSortedReverse == td.rSortedReverse

        assert rDistinctSorted == td.rDistinctSorted

        
    def test_getColumnDataFromSql(self):
        """
        Test getColumnDataFromSql.
        """

        rSql = self.pgi.getColumnDataFromSql("select area from data.municipio where area<5000000 order by area")
        self.pgi.close()

        assert rSql == td.sql


    def test_analyzeGeomColumnFromTable(self):
        """
        Test analyzeGeomColumnFromTable.
        """

        r = self.pgi.analyzeGeomColumnFromTable("data", "municipio", "geom")
        self.pgi.close()
        
        assert r=={'ymax': 4288702.72162018, 'xmin': 100401.207748027,
                   'xmax': 621272.560611986, 'srid': 25830, 'ymin': 3977032.24536145,
                   'type': 'ST_MultiPolygon'}
        

    def test_analyzeGeomColumnFromSql(self):
        """
        Test analyzeGeomColumnFromSql.
        """

        r = self.pgi.analyzeGeomColumnFromSql("select * from data.municipio", "geom")
        self.pgi.close()
        
        assert r=={'ymax': 4288702.72162018, 'xmin': 100401.207748027,
                   'xmax': 621272.560611986, 'srid': 25830, 'ymin': 3977032.24536145,
                   'type': 'ST_MultiPolygon'}


    def test_getPgDataTypes(self):
        """
        Test getPgDataTypes.
        """

        r = self.pgi.getPgDataTypes()
        self.pgi.close()

        assert r[1043]=="varchar"
        assert r[23]=="int4"
