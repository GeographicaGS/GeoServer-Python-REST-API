#!/usr/bin/env python
# coding=UTF-8

import geoserverapirest.core as gs
reload(gs)

"""
Requires the Docker-Compose to be up.
"""

class TestDeletion(object):
    """
    Deletion tests.
    """

    def setup(self):
        self.gsi = gs.GsInstance("http://localhost:8084/geoserver", "admin", "geoserver")

        
    def test_deleteStyle(self):
        r = self.gsi.deleteStyle("new_style")
        assert r==200


    def test_deleteFeatureType(self):
        r = self.gsi.deleteFeatureType("new_featuretype")
        assert r==200
        

    def test_deleteDatastore(self):
        r = self.gsi.deleteDatastore("new_workspace", "new_postgis_ds")
        assert r==200
        
        
    def test_deleteWorkspace(self):
        r = self.gsi.deleteWorkspace("new_workspace")
        assert r==200
