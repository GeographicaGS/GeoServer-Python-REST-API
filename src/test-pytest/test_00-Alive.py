#!/usr/bin/env python
# coding=UTF-8

# import unittest as t, time
import geoserverapirest.core as gs
reload(gs)

"""
Requires two GeoServers for testing. Check Docker-Compose.
"""

class TestAlive:
    """
    Tests a GeoServer instance.
    """

    def setup(self):
        self.gsi = gs.GsInstance("http://localhost:8084/geoserver", "admin", "geoserver")

        
    def test_checkAliveA(self):
        assert self.gsi.checkAlive()==200


    def test_notAlive(self):
        ins = gs.GsInstance("http://localhost:9999/geoserver", "admin", "geoserver")
        assert ins.checkAlive()==404

        
    def test_aliveNotAGeoServer(self):
        ins = gs.GsInstance("http://www.google.com", "admin", "geoserver")
        assert ins.checkAlive()==404

        
    def test_getUrl(self):
        assert self.gsi.url=="http://localhost:8084/geoserver"

        
    def test_getUser(self):
        assert self.gsi.user=="admin"

        
    def test_getPasswd(self):
        assert self.gsi.passwd=="geoserver"
