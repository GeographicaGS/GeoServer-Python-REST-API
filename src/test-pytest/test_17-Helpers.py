#!/usr/bin/env python
# coding=UTF-8

import geoserverapirest.ext.sld as sld
import geoserverapirest.ext.postgis as pgis
reload(sld)
reload(pgis)

"""
Requires two GeoServers for testing. Check Docker-Compose.

THIS TESTS ARE MEANT TO BE RUN INSIDE THE PYTHON-TEST CONTAINER OF THE DOCKER COMPOSE.
"""

class TestHelpers:
    """
    Helpers testers.
    """

    def setup(self):
        self.pgisC = pgis.GsPostGis("db", 5432, "test_geoserver", "postgres", "postgres")
        self.sldC = sld.GsSld()


    def test_getMinMaxFromPgColumn(self):
        r = self.pgisC.getColumnMinMax("data.municipio;delete from data.municipio;", "area")

        
        
        
    def test_createCategorizedSld(self):
        # Min inteval, max interval, intervals, precision
        r = self.sldC.equalInterval(2.67, 2.77, 5, 2)

        assert r==[[2.67, 2.68], [2.69, 2.7], [2.71, 2.72], [2.73, 2.74], [2.75, 2.77]]

        
    # def test_createPostGisLayer(self):
    #     r = self.ghpg.createPostGisLayer("new_workspace", "new_postgis_ds", "municipio", \
    #                                      "municipio", "Municipios de Andalucía por extensión", \
    #                                      "postgres", 25830, style, nativeCRS=25830)

    #     print r
