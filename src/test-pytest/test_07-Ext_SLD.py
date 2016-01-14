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
        
        assert str(s)=="""<?xml version='1.0' encoding='UTF-8'?>\n<ns0:StyledLayerDescriptor xmlns:ns0="http://www.opengis.net/sld" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.1.0" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.1.0/StyledLayerDescriptor.xsd" />"""


    def test_createSldNamedLayer(self):
        """
        Test creation of SLD named layer.
        """

        s = sld.GsSldNamedLayer("aNamedLayer")

        assert str(s)=="""<?xml version='1.0' encoding='UTF-8'?>\n<ns0:NamedLayer xmlns:ns0="http://www.opengis.net/sld" xmlns:ns1="http://www.opengis.net/se"><ns1:Name>aNamedLayer</ns1:Name></ns0:NamedLayer>"""


    def test_createUserStyle(self):
        """
        Test creation of SLD user style.
        """

        s = sld.GsSldUserStyle("aUserStyle")

        assert str(s)=="""<?xml version='1.0' encoding='UTF-8'?>\n<ns0:UserStyle xmlns:ns0="http://www.opengis.net/sld" xmlns:ns1="http://www.opengis.net/se"><ns1:Name>aUserStyle</ns1:Name></ns0:UserStyle>"""
        

    def test_createFeatureTypeStyle(self):
        """
        Test creation of a feature type style.
        """

        s = sld.GsSldFeatureTypeStyle()
        
        assert str(s)=="""<?xml version='1.0' encoding='UTF-8'?>\n<ns0:FeatureTypeStyle xmlns:ns0="http://www.opengis.net/se" />"""
        

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

        assert str(s)=="""<?xml version='1.0' encoding='UTF-8'?>\n<ns0:Rule xmlns:ns0="http://www.opengis.net/se"><ns0:Name>aRule</ns0:Name><ns0:Description><ns0:Title>aRule description</ns0:Title></ns0:Description></ns0:Rule>"""
        

    def test_createStrokeSymbolizer(self):
        """
        Test creation of a stroke symbolizer.
        """

        s = sld.GsSldStrokeSymbolizer("#001100", 0.5, "bevel")

        assert str(s)=="""<?xml version='1.0' encoding='UTF-8'?>\n<ns0:Stroke xmlns:ns0="http://www.opengis.net/se"><ns0:SvgParameter name="stroke">#001100</ns0:SvgParameter><ns0:SvgParameter name="stroke-width">0.5</ns0:SvgParameter><ns0:SvgParameter name="stroke-linejoin">bevel</ns0:SvgParameter></ns0:Stroke>"""


    def test_createFillSymbolizer(self):
        """
        Test creation of a fill symbolizer.
        """

        s = sld.GsSldFillSymbolizer("#009922")

        assert str(s)=="""<?xml version='1.0' encoding='UTF-8'?>\n<ns0:Fill xmlns:ns0="http://www.opengis.net/se"><ns0:SvgParameter name="fill">#009922</ns0:SvgParameter></ns0:Fill>"""


    def test_createPolygonSymbolizer(self):
        """
        Test creation of a polygon symbolizer.
        """

        s = sld.GsSldPolygonSymbolizer()

        assert str(s)=="""<?xml version='1.0' encoding='UTF-8'?>\n<ns0:PolygonSymbolizer xmlns:ns0="http://www.opengis.net/se" />"""


    def test_rangesEqualInterval(self):
        """
        Test equal interval output.
        """

        s = sld.Range()
        
        assert s.equalInterval(1, 15, 4, 2)== \
            [[1.0, 4.49], [4.5, 7.99], [8.0, 11.49], [11.5, 15]]
        

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

        assert str(root)=="""<?xml version='1.0' encoding='UTF-8'?>\n<ns0:StyledLayerDescriptor xmlns:ns0="http://www.opengis.net/sld" xmlns:ns2="http://www.opengis.net/se" xmlns:ns3="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.1.0" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.1.0/StyledLayerDescriptor.xsd"><ns0:NamedLayer><ns2:Name>municipio</ns2:Name><ns0:UserStyle><ns2:Name>municipio</ns2:Name><ns2:FeatureTypeStyle><ns2:Rule><ns2:Name>A rule</ns2:Name><ns2:Description><ns2:Title>This is a rule</ns2:Title></ns2:Description><ns3:Filter><ns3:And><ns3:PropertyIsGreaterThan><ns3:PropertyName>area</ns3:PropertyName><ns3:Literal>3</ns3:Literal></ns3:PropertyIsGreaterThan><ns3:PropertyIsLessThanOrEqualTo><ns3:PropertyName>area</ns3:PropertyName><ns3:Literal>4</ns3:Literal></ns3:PropertyIsLessThanOrEqualTo></ns3:And></ns3:Filter><ns2:PolygonSymbolizer><ns2:Fill><ns2:SvgParameter name="fill">#000000</ns2:SvgParameter></ns2:Fill><ns2:Stroke><ns2:SvgParameter name="stroke">#000000</ns2:SvgParameter><ns2:SvgParameter name="stroke-width">0.25</ns2:SvgParameter><ns2:SvgParameter name="stroke-linejoin">bevel</ns2:SvgParameter></ns2:Stroke></ns2:PolygonSymbolizer></ns2:Rule></ns2:FeatureTypeStyle></ns0:UserStyle></ns0:NamedLayer></ns0:StyledLayerDescriptor>"""
