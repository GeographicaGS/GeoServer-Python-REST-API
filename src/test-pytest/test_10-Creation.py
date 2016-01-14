#!/usr/bin/env python
# coding=UTF-8

import geoserverapirest.core as gs
reload(gs)
import geoserverapirest.ext.postgis as pg
reload(pg)
import geoserverapirest.ext.sld as sld
reload(sld)

"""
Requires two GeoServers for testing. Check Docker-Compose.

THIS TESTS ARE MEANT TO BE RUN INSIDE THE PYTHON-TEST CONTAINER OF THE DOCKER COMPOSE.
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
					<PointSymbolizer>
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
        self.gsi = gs.GsInstance("http://sourcegeoserver:8080/geoserver", "admin", "geoserver")

        
    def test_createWorkspace(self):
        r = self.gsi.createWorkspace("new_workspace")
        assert r==201


    def test_createPostGisDataStore(self):
        r = self.gsi.createPostGisDataStore("new_workspace", "new_postgis_ds", \
                                            "db", "5432", \
                                            "postgres", "postgres", "test_geoserver", \
                                            "data")
        assert r==201


    def test_createFeatureTypeFromPostGisTable(self):
        r = self.gsi.createFeatureTypeFromPostGisTable("new_workspace", \
                                                       "new_postgis_ds", "municipio", \
                                                       "geom", "municipio", \
                                                       u"Municipios de Andalucía", \
                                                       "postgres")
        
        assert r==201


    def test_createFeatureTypeFromPostGisQuery(self):
        sql = """select * from data.municipio where "PROVINCIA"='Sevilla'"""
        
        r = self.gsi.createFeatureTypeFromPostGisQuery("new_workspace", \
                                                       "new_postgis_ds", sql, \
                                                       "gid", "geom", "MultiPolygon", \
                                                       "municipios_sevilla", \
                                                       "Municipios de Sevilla", \
                                                       "postgres")

        assert r==201

        sql = """select * from data.municipio where "PROVINCIA"='Córdoba'"""
        
        r = self.gsi.createFeatureTypeFromPostGisQuery("new_workspace", \
                                                       "new_postgis_ds", sql, \
                                                       "gid", "geom", "MultiPolygon", \
                                                       "municipios_cordoba", \
                                                       "Municipios de Córdoba", \
                                                       "postgres")

        assert r==201

                            
    def test_createStyle(self):
        r = self.gsi.createStyle("new_style", self.sld)
        assert r==200


    def test_updateLayer(self):
        r = self.gsi.updateLayer("municipio", styles=["polygon", "line", "point"])
        assert r==200


    def test_createComplexLayer(self):
        """
        Creates a complex style based on a double color ramp from a column in PostgreSQL.
        """

        # Take range in PostgreSQL column
        pgi = pg.GsPostGis("db", "5432", "test_geoserver", "postgres", "postgres")
        r = pgi.getColumnMinMax("data", "municipio", "area")
        pgi.close()

        # Create first part of the color ramp, up to a data of 3.000.000, in 5 steps
        s = sld.Range()
        range00 = s.equalInterval(r[0], 3000000, 5, 2)

        # Modify the lowest interval a little bit, so SLD conditions take into
        # account the smallest area
        range00[0][0] = range00[0][0]-0.01

        color = sld.Color()
        cr00 = color.colorRamp("#a6611a", "#f0e9da", 5)

        # Create the second part of the color ramp, from 3.000.000 to up, in 5 steps
        # Create 6 colors to discart the first one when joining the two parts of the
        # ramp
        range01 = s.equalInterval(3000000.01, r[1], 5, 2)
        cr01 = color.colorRamp("#f0e9da", "#018571", 6)

        range00.extend(range01)
        cr00.extend(cr01[1:])

        # Generate stroke symbol
        stroke = sld.GsSldStrokeSymbolizer("#333333", 0.1, "bevel")

        # The final featureTypeStyle
        featureTypeStyle = sld.GsSldFeatureTypeStyle()
        
        # Generate ruled style
        for i in range(0,10):
            # Generate fill
            fill = sld.GsSldFillSymbolizer(cr00[i])

            # Generate poly symbol
            poly = sld.GsSldPolygonSymbolizer()
            poly.addSymbol(fill)
            poly.addSymbol(stroke)

            # Generate rule condition
            c0 = sld.GsSldCondition("GT", "area", range00[i][0])
            c1 = sld.GsSldCondition("LTOE", "area", range00[i][1])
            c0.composite(c1, "And")

            # Generate the filter
            filter = sld.GsSldFilter()
            filter.addCondition(c0)

            # Create rule
            rule = sld.GsSldRule("Areas %s" % i, \
                                 "Municipios con área entre %s y %s" % \
                                 (range00[i][0], range00[i][1]))
            rule.addSymbolizer(poly)
            rule.addFilter(filter)

            featureTypeStyle.addRule(rule)

        # Create user style
        userStyle = sld.GsSldUserStyle("municipio_area")
        userStyle.addFeatureTypeStyle(featureTypeStyle)

        # Create named layer
        namedLayer = sld.GsSldNamedLayer("municipio_area")
        namedLayer.addUserStyle(userStyle)

        # Final SLD
        root = sld.GsSldRoot()
        root.addNamedLayer(namedLayer)
            
        # Upload style
        gsresponse = self.gsi.createStyle("municipio_area", str(root))
        assert gsresponse==200

        # Create feature type from PostGIS table
        ft = self.gsi.createFeatureTypeFromPostGisTable("new_workspace", \
                                                        "new_postgis_ds", \
                                                        "municipio", \
                                                        "geom", "municipios_area",
                                                        u"Municipios de Andalucía por área", \
                                                        "postgres")

        assert ft==201

        gsresponse = self.gsi.updateLayer("municipios_area", styles=["municipio_area"], \
                                          defaultStyle="municipio_area")

        assert gsresponse==200
        
