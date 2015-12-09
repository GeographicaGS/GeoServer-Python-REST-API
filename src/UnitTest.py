#!/usr/bin/env python
# coding=UTF-8

import unittest as t, time
import geoserverapirest.core as gs
reload(gs)

"""
Requires two GeoServers for testing. Check Docker-Compose.
"""

class TestAlive(t.TestCase):
    """
    Tests a GeoServer instance.
    """

    def setUp(self):
        self.instanceA = gs.GsInstance("http://localhost:8084/geoserver", "admin", "geoserver")
        self.instanceB = gs.GsInstance("http://localhost:8085/geoserver", "admin", "geoserver")

    def test_checkAliveA(self):
        self.assertEqual(self.instanceA.checkAlive(), 200)

    def test_checkAliveB(self):
        self.assertEqual(self.instanceB.checkAlive(), 200)

    def test_notAlive(self):
        ins = gs.GsInstance("http://localhost:9999/geoserver", "admin", "geoserver")
        self.assertEqual(ins.checkAlive(), 404)

    def test_aliveNotAGeoServer(self):
        ins = gs.GsInstance("http://www.google.com", "admin", "geoserver")
        self.assertEqual(ins.checkAlive(), 404)

    def test_getUrl(self):
        self.assertEqual(self.instanceA.url, "http://localhost:8084/geoserver")

    def test_getUser(self):
        self.assertEqual(self.instanceA.user, "admin")

    def test_getPasswd(self):
        self.assertEqual(self.instanceA.passwd, "geoserver")

        

class TestCreation(t.TestCase):
    """
    Object creation tests.
    """
    
    def setUp(self):
        self.sld = """
        <?xml version="1.0" encoding="ISO-8859-1"?>
          <StyledLayerDescriptor version="1.0.0" 
            xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" 
            xmlns="http://www.opengis.net/sld" 
            xmlns:ogc="http://www.opengis.net/ogc" 
            xmlns:xlink="http://www.w3.org/1999/xlink" 
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <!-- a named layer is the basic building block of an sld document -->

            <NamedLayer>
              <Name>Default Point</Name>
              <UserStyle>
                <!-- they have names, titles and abstracts -->
		  
                <Title>A boring default style</Title>
                <Abstract>A sample style that just prints out a purple square</Abstract>
                <!-- FeatureTypeStyles describe how to render different features -->
                <!-- a feature type for points -->

                <FeatureTypeStyle>
                  <!--FeatureTypeName>Feature</FeatureTypeName-->
                  <Rule>
                    <Name>Rule 1</Name>
					<Title>RedSquare</Title>
					<Abstract>A red fill with an 11 pixel size</Abstract>

					<!-- like a linesymbolizer but with a fill too -->
					<PoinntSymbolizer>
                      <Graphic>
                        <Mark>
                          <WellKnownName>square</WellKnownName>
                          <Fill>
                            <CssParameter name="fill">#FF0000</CssParameter>
                          </Fill>
                        </Mark>
                        <Size>6</Size>
                      </Graphic>
					</PointSymbolizer>
                  </Rule>
                </FeatureTypeStyle>
              </UserStyle>
            </NamedLayer>
          </StyledLayerDescriptor>
        """
        self.instanceA = gs.GsInstance("http://localhost:8084/geoserver", "admin", "geoserver")
        
    def test_createWorkspace(self):
        r = self.instanceA.createWorkspace("new_workspace")
        self.assertEqual(r, 201)
        r = self.instanceA.getWorkspaceNames()
        self.assertSetEqual(set(r), set([u"new_workspace"]))


    def test_createStyle(self):
        r = self.instanceA.createStyle("new_style", self.sld)
        self.assertEqual(r, 200)
        self.assertSetEqual(set(self.instanceA.getStyleNames()), \
                            set([u"point", u"line", u"polygon", u"raster", u"new_style"]))



class TestDeletion(t.TestCase):
    """
    Deletion tests.
    """
    def setUp(self):
        self.instanceA = gs.GsInstance("http://localhost:8084/geoserver", "admin", "geoserver")

    def test_deleteStyle(self):
        r = self.instanceA.deleteStyle("new_style")
        self.assertEqual(r, 200)
        self.assertSetEqual(set(self.instanceA.getStyleNames()), \
                            set([u"point", u"line", u"polygon", u"raster"]))

    def test_deleteWorkspace(self):
        r = self.instanceA.deleteWorkspace("new_workspace")
        self.assertEqual(r, 200)
        r = self.instanceA.getWorkspaceNames()
        self.assertSetEqual(set(r), set([]))







                
                         
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
        
