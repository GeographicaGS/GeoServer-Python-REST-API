#!/usr/bin/env python
# coding=UTF-8

import geoserverapirest.core as gs
reload(gs)

"""
Requires the Docker-Compose to be up.

THIS TESTS ARE MEANT TO BE RUN INSIDE THE PYTHON-TEST CONTAINER OF THE DOCKER COMPOSE.
"""

class TestDeletion(object):
    """
    Deletion tests.
    """

    def setup(self):
        self.gsi = gs.GsInstance("http://sourcegeoserver:8080/geoserver", "admin", "geoserver")

        
    def test_deleteFeatureType(self):
        for i in ["municipio", "municipios_sevilla", "municipios_cordoba", \
                  "municipios_area", "municipios_area_jenks", "municipios_area_monoramp", \
                  "municipios_area_dualramp", "municipio_area_comp_quartile", \
                  "municipio_area_comp_equal", "municipio_area_comp_jenks", \
                  "municipios_area_monorampnoborder", "municipio_automate_test_00", \
                  "municipio_automate_test_01"]:       
            r = self.gsi.deleteFeatureType("new_workspace", "new_postgis_ds", \
                                           i, recurse=True)                                       
            assert r==200
        

    def test_deleteDatastore(self):
        r = self.gsi.deleteDatastore("new_workspace", "new_postgis_ds")
        assert r==200
        
        
    def test_deleteWorkspace(self):
        r = self.gsi.deleteWorkspace("new_workspace")
        assert r==200


    def test_deleteStyle(self):
        for i in ["new_style", "municipio_area", "municipio_area_jenks", \
                  "municipio_area_monoramp", "municipio_area_monorampnoborder", \
                  "municipio_area_dualramp", "municipio_area_comp_equal", \
                  "municipio_area_comp_jenks", "municipio_area_comp_quartile", \
                  "test_automate_00", "test_automate_01", "test_automate_02"]:
            r = self.gsi.deleteStyle(i)
            assert r==200
