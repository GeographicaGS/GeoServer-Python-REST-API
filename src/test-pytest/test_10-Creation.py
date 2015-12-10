#!/usr/bin/env python
# coding=UTF-8

# import unittest as t, time
import geoserverapirest.core as gs
reload(gs)

"""
Requires two GeoServers for testing. Check Docker-Compose.
"""

class TestCreation:
    """
    Object creation tests.
    """

    def setup(self):
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
        self.gsi = gs.GsInstance("http://localhost:8084/geoserver", "admin", "geoserver")

        
    def test_createWorkspace(self):
        r = self.gsi.createWorkspace("new_workspace")
        assert r==201


    def test_createPostGisDataStore(self):
        r = self.gsi.createPostGisDataStore("new_workspace", "new_postgis_ds", \
                                            "db", "5432", \
                                            "postgres", "postgres", "test_geoserver", \
                                            "data")
        assert r==201


    def test_createFeatureType(self):
        r = self.gsi.createFeatureTypeFromPostGisTable("new_workspace", \
                                                   "new_postgis_ds", "data.municipio", \
                                                   "municipio", u"Municipios de Andalucía")
        
        assert r==201

        
    def test_createStyle(self):
        r = self.gsi.createStyle("new_style", self.sld)
        assert r==200

