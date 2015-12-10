
        

#!/usr/bin/env python
# coding=UTF-8

# import unittest as t, time
import geoserverapirest.core as gs
reload(gs)

"""
Requires two GeoServers for testing. Check Docker-Compose.
"""

class TestDeletion:
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








                
                         
# Class TestWorkspace(t.TestCase):
#     """
#     Tests workspaces.
#     """

#     def setUp(self):
#         self.workspace = gs.GsWorkspace("new_workspace")

#     def test_create(self):
#         self.assertIsInstance(self.workspace, gs.GsWorkspace)

    
                                 


        
# class TestLayers(t.TestCase):
#     """
#     Tests layers.
#     """

#     def setUp(self):
#         self.layer = gs.GsLayer("new_layer")

#     def test_create(self):
#         self.assertIsInstance(self.layer, gs.GsLayer)

#     def test_getLayerName(self):
#         self.assertEqual(self.layer.name, "new_layer")
        
