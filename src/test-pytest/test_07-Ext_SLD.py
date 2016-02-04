#!/usr/bin/env python
# coding=UTF-8

import geoserverapirest.ext.sld as sld
reload(sld)

"""
Requires the Docker-Compose to be up.

THIS TESTS ARE MEANT TO BE RUN INSIDE THE PYTHON-TEST CONTAINER OF THE DOCKER COMPOSE.
"""

class TestExtSld:
    """
    ext SLD test suite.
    """
    
    def setup(self):
        pass


    def test_createSldRoot(self):
        """
        Test creation of SLD root.
        """

        s = sld.GsSldRoot()
        
        assert str(s)=="""<?xml version='1.0' encoding='UTF-8'?>\n<ns0:StyledLayerDescriptor xmlns:ns0="http://www.opengis.net/sld" version="1.0.0" />"""


    def test_createSldNamedLayer(self):
        """
        Test creation of SLD named layer.
        """

        s = sld.GsSldNamedLayer("aNamedLayer")

        assert str(s)=="""<?xml version='1.0' encoding='UTF-8'?>\n<NamedLayer><Name>aNamedLayer</Name></NamedLayer>"""


    def test_createUserStyle(self):
        """
        Test creation of SLD user style.
        """

        s = sld.GsSldUserStyle("aUserStyle")
        
        assert str(s)=="""<?xml version='1.0' encoding='UTF-8'?>\n<UserStyle><Name>aUserStyle</Name></UserStyle>"""
        

    def test_createFeatureTypeStyle(self):
        """
        Test creation of a feature type style.
        """

        s = sld.GsSldFeatureTypeStyle()

        assert str(s)=="""<?xml version='1.0' encoding='UTF-8'?>\n<FeatureTypeStyle />"""
        

    def test_createCondition(self):
        """
        Test creation of a condition.
        """

        s = sld.GsSldCondition("GT", "afield", "30.2")
        
        assert str(s)=="""<?xml version='1.0' encoding='UTF-8'?>\n<ns0:PropertyIsGreaterThan xmlns:ns0="http://www.opengis.net/ogc"><ns0:PropertyName>afield</ns0:PropertyName><ns0:Literal>30.2</ns0:Literal></ns0:PropertyIsGreaterThan>"""


    def test_createFilter(self):
        """
        Test creation of a filter.
        """

        s = sld.GsSldFilter()

        assert str(s)=="""<?xml version='1.0' encoding='UTF-8'?>\n<ns0:Filter xmlns:ns0="http://www.opengis.net/ogc" />"""
        

    def test_createRule(self):
        """
        Test creation of a rule.
        """

        s = sld.GsSldRule("aRule", "aRule description")

        assert str(s)=="""<?xml version='1.0' encoding='UTF-8'?>\n<Rule><Name>aRule</Name><Title>aRule description</Title></Rule>"""
        

    def test_createStrokeSymbolizer(self):
        """
        Test creation of a stroke symbolizer.
        """

        s = sld.GsSldStrokeSymbolizer("#001100", 0.5, "bevel")
        
        assert str(s)=="""<?xml version='1.0' encoding='UTF-8'?>\n<Stroke><CssParameter name="stroke">#001100</CssParameter><CssParameter name="stroke-width">0.5</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke>"""


    def test_createFillSymbolizer(self):
        """
        Test creation of a fill symbolizer.
        """

        s = sld.GsSldFillSymbolizer("#009922")
        
        assert str(s)=="""<?xml version='1.0' encoding='UTF-8'?>\n<Fill><CssParameter name="fill">#009922</CssParameter></Fill>"""


    def test_createPolygonSymbolizer(self):
        """
        Test creation of a polygon symbolizer.
        """

        s = sld.GsSldPolygonSymbolizer()
        
        assert str(s)=="""<?xml version='1.0' encoding='UTF-8'?>\n<PolygonSymbolizer />"""


    def test_rangesEqualInterval(self):
        """
        Test equal interval output.
        """

        s = sld.Range()
        
        assert s.equalInterval([1,3,5,3,4,15], 4, 2)== \
            [[1.0, 4.49], [4.5, 7.99], [8.0, 11.49], [11.5, 15]]


    def test_rangesJenksInterval(self):
        """
        Test Jenks interval output.
        """

        s = sld.Range()
        
        assert s.jenksInterval([4,5,9,10,3,2,3,4,3,3,3,32,2,3,3,2,3,3,4,3,2,2,3,3,3,2,3,3,3,2,2,3,3,2], \
                               7, 1, adjust=0.95)== \
                               [[2.0, 2.9], [3.0, 9.9], [10.0, 32.0]]
                                
        assert s.jenksInterval([4,5,9,10], \
                               3, 1, adjust=0.95)==[[4.0, 4.9], [5.0, 8.9], [9.0, 10.0]]


    def test_createColorRamp(self):
        """
        Test the creation of a color ramp.
        """

        s = sld.Color()
        cr = s.colorRamp("#2812ef", "#8e2f9c", 10)

        assert cr==['#2812ef', '#3b15e6', '#4e19dc', '#5d1dd2', '#6b20c9', '#7624bf', '#7f27b6', '#862aad', '#8b2ca5', '#8e2f9c']

        
    def test_createFullSld00(self):
        """
        Test creation of a full SLD parseable by GeoServer 2.8.2.
        """

        # Creates polygon symbol
        fill = sld.GsSldFillSymbolizer("#000000")
        stroke = sld.GsSldStrokeSymbolizer("#000000", 0.25, "bevel")
        polySym = sld.GsSldPolygonSymbolizer()
        polySym.addSymbol(fill)
        polySym.addSymbol(stroke)

        # Creates rule condition
        c1 = sld.GsSldCondition("GT", "area", 3)
        c2 = sld.GsSldCondition("LTOE", "area", 4)
        c1.composite(c2, "And")
        filter = sld.GsSldFilter()
        filter.addCondition(c1)

        # Create rule
        rule = sld.GsSldRule("A rule", "This is a rule")
        rule.addSymbolizer(polySym)
        rule.addFilter(filter)

        # Put everything together
        featureTypeStyle = sld.GsSldFeatureTypeStyle()
        featureTypeStyle.addRule(rule)
        userStyle = sld.GsSldUserStyle("municipio")
        userStyle.addFeatureTypeStyle(featureTypeStyle)
        namedLayer = sld.GsSldNamedLayer("municipio")
        namedLayer.addUserStyle(userStyle)

        root = sld.GsSldRoot()
        root.addNamedLayer(namedLayer)

        assert str(root)=="""<?xml version='1.0' encoding='UTF-8'?>\n<ns0:StyledLayerDescriptor xmlns:ns0="http://www.opengis.net/sld" xmlns:ns1="http://www.opengis.net/ogc" version="1.0.0"><NamedLayer><Name>municipio</Name><UserStyle><Name>municipio</Name><FeatureTypeStyle><Rule><Name>A rule</Name><Title>This is a rule</Title><ns1:Filter><ns1:And><ns1:PropertyIsGreaterThan><ns1:PropertyName>area</ns1:PropertyName><ns1:Literal>3</ns1:Literal></ns1:PropertyIsGreaterThan><ns1:PropertyIsLessThanOrEqualTo><ns1:PropertyName>area</ns1:PropertyName><ns1:Literal>4</ns1:Literal></ns1:PropertyIsLessThanOrEqualTo></ns1:And></ns1:Filter><PolygonSymbolizer><Fill><CssParameter name="fill">#000000</CssParameter></Fill><Stroke><CssParameter name="stroke">#000000</CssParameter><CssParameter name="stroke-width">0.25</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke></PolygonSymbolizer></Rule></FeatureTypeStyle></UserStyle></NamedLayer></ns0:StyledLayerDescriptor>"""
        





