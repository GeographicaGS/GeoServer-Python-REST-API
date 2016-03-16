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


    def test_buildRuleTitles(self):
        """
        Test function buildRuleTitles.
        """

        s = sld.GsSldStyles()

        ranges = [[1.223, 2.112],[2.113, 2.443],[2.444, 2.999],[3,3],[3.001, 4.232]]
        
        assert s.buildRuleTitles(ranges, "From %s to %s", "Strictly %s", \
                                 ruleTitleLambdas=lambda x: round(x, 1))== \
                                 ['From 1.2 to 2.1', 'From 2.1 to 2.4', 'From 2.4 to 3.0', \
                                  'Strictly 3.0', 'From 3.0 to 4.2']
        

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

        rule = sld.GsSldConditionAnd(
            sld.GsSldConditionGtoe("afield", 30.2),
            sld.GsSldConditionLtoe("afield", 40.2))

        assert str(rule)=="""<?xml version='1.0' encoding='UTF-8'?>\n<ns0:And xmlns:ns0="http://www.opengis.net/ogc"><ns0:PropertyIsLessThanOrEqualTo><ns0:PropertyName>afield</ns0:PropertyName><ns0:Literal>40.2</ns0:Literal></ns0:PropertyIsLessThanOrEqualTo><ns0:PropertyIsGreaterThanOrEqualTo><ns0:PropertyName>afield</ns0:PropertyName><ns0:Literal>30.2</ns0:Literal></ns0:PropertyIsGreaterThanOrEqualTo></ns0:And>"""

        rule = sld.GsSldConditionOr(
            sld.GsSldConditionAnd(
                sld.GsSldConditionEqual("afield", "Córdoba"),
                sld.GsSldConditionAnd(
                    sld.GsSldConditionGtoe("anotherfield", 30.2),
                    sld.GsSldConditionLtoe("anotherfield", 40.2))
            ),
            sld.GsSldConditionEqual("afield", "Sevilla"))
                    
        assert str(rule)=="""<?xml version='1.0' encoding='UTF-8'?>\n<ns0:Or xmlns:ns0="http://www.opengis.net/ogc"><ns0:PropertyIsEqualTo><ns0:PropertyName>afield</ns0:PropertyName><ns0:Literal>Sevilla</ns0:Literal></ns0:PropertyIsEqualTo><ns0:And><ns0:And><ns0:PropertyIsLessThanOrEqualTo><ns0:PropertyName>anotherfield</ns0:PropertyName><ns0:Literal>40.2</ns0:Literal></ns0:PropertyIsLessThanOrEqualTo><ns0:PropertyIsGreaterThanOrEqualTo><ns0:PropertyName>anotherfield</ns0:PropertyName><ns0:Literal>30.2</ns0:Literal></ns0:PropertyIsGreaterThanOrEqualTo></ns0:And><ns0:PropertyIsEqualTo><ns0:PropertyName>afield</ns0:PropertyName><ns0:Literal>Córdoba</ns0:Literal></ns0:PropertyIsEqualTo></ns0:And></ns0:Or>"""

        s = sld.GsSldConditionGtoe("afield", "30.2")
        
        assert str(s)=="""<?xml version='1.0' encoding='UTF-8'?>\n<ns0:PropertyIsGreaterThanOrEqualTo xmlns:ns0="http://www.opengis.net/ogc"><ns0:PropertyName>afield</ns0:PropertyName><ns0:Literal>30.2</ns0:Literal></ns0:PropertyIsGreaterThanOrEqualTo>"""

        s = sld.GsSldConditionLtoe("afield", "30.2")
        
        assert str(s)=="""<?xml version='1.0' encoding='UTF-8'?>\n<ns0:PropertyIsLessThanOrEqualTo xmlns:ns0="http://www.opengis.net/ogc"><ns0:PropertyName>afield</ns0:PropertyName><ns0:Literal>30.2</ns0:Literal></ns0:PropertyIsLessThanOrEqualTo>"""


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


    def test_rangesQuartileInterval(self):
        """
        Test quartile interval output.
        """

        s = sld.Range()

        data = [2,1,3,4,2,1,3,5,6,7,54,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,3,3,3,3,3,4,4,4,4,5,5,5,6,6,7,8,8,8,8,7,56,44,34,332,232,32,332,231,1001]

        assert s.quartileInterval(data, 4, 1)== \
          [[1, 1], [2, 3], [4, 6], [7, 1001]]
        

    def test_rangesJenksInterval(self):
        """
        Test Jenks interval output.
        """

        s = sld.Range()

        data = [2,1,3,4,2,1,3,5,6,7,54,7,56,44,34,332,232,32,332,231,1001]

        assert s.jenksInterval(data, 1, 0) == [[1.0, 1001.0]]
        
        assert s.jenksInterval(data, 2, 0) == [[1.0, 332.0], [1001.0, 1001.0]]
           
        assert s.jenksInterval(data, 3, 0) == [[1.0, 56.0], [231.0, 332.0], [1001.0, 1001.0]]

        assert s.jenksInterval(data, 4, 0) == [[1.0, 56.0], [231.0, 232.0], \
                                              [332.0, 332.0], [1001.0, 1001.0]]
                                              
        assert s.jenksInterval(data, 5, 0) == [[1.0, 7.0], [32.0, 56.0], [231.0, 232.0], \
                                               [332.0, 332.0], [1001.0, 1001.0]]

        assert s.jenksInterval(data, 6, 0) in [[[1.0, 7.0], [32.0, 44.0], [54.0, 56.0], \
                                                [231.0, 232.0], [332.0, 332.0], [1001.0, 1001.0]], \
                                                [[1.0, 7.0], [32.0, 34.0], [44.0, 56.0], \
                                                [231.0, 232.0], [332.0, 332.0], [1001.0, 1001.0]]]

        assert s.jenksInterval(data, 7, 0) == [[1.0, 7.0], [32.0, 34.0], [44.0, 44.0], \
                                               [54.0, 56.0], [231.0, 232.0], \
                                               [332.0, 332.0], [1001.0, 1001.0]]

        assert s.jenksInterval(data, -1, 0) == None

        assert s.jenksInterval(data, 17, 0) == None


    def test_rangesJenksMiddleInterval(self):
        """
        Test Jenks with a middle breaking value.
        """

        s = sld.Range()

        data = [2,1,3,4,2,1,3,5,6,7,54,7,56,44,34,332,232,32,332,231,1001]

        assert s.jenksMiddleInterval(data, 4, 50, 0) in [[[1.0, 3.0], [4.0, 7.0], [32.0, 34.0], \
                                                          [44.0, 44.0], [50, 50], [54.0, 56.0], \
                                                          [231.0, 232.0], [332.0, 332.0], \
                                                          [1001.0, 1001.0]],
                                                         [[1.0, 4.0], [5.0, 7.0], [32.0, 34.0], \
                                                          [44.0, 44.0], [50, 50], [54.0, 56.0], \
                                                          [231.0, 232.0], [332.0, 332.0], \
                                                          [1001.0, 1001.0]]]
        
        
    def test_createColorRamp(self):
        """
        Test the creation of a color ramp.
        """

        s = sld.Color()
        cr = s.colorRamp("#2812ef", "#8e2f9c", 10)

        assert cr==['#2812ef', '#3b15e6', '#4e19dc', '#5d1dd2', '#6b20c9', '#7624bf', '#7f27b6', '#862aad', '#8b2ca5', '#8e2f9c']


    def test_createDualColorRamp(self):
        """
        Test the creation of a dual color ramp.
        """

        s = sld.Color()
        cr = s.colorDualRamp("#2812ef", "#ffffff", "#8e2f9c", 4)
        
        assert cr==['#2812ef', '#62d5de', '#a4dba7', '#e6e6d8', '#ffffff', '#dcded3', \
                    '#9ec7b0', '#5e7eba', '#8e2f9c']

        
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
        cond = sld.GsSldConditionAnd(
            sld.GsSldConditionGtoe("area", 3),
            sld.GsSldConditionLtoe("area", 4))
        
        filter = sld.GsSldFilter()
        filter.addCondition(cond)

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

        assert str(root)=="""<?xml version='1.0' encoding='UTF-8'?>\n<ns0:StyledLayerDescriptor xmlns:ns0="http://www.opengis.net/sld" xmlns:ns1="http://www.opengis.net/ogc" version="1.0.0"><NamedLayer><Name>municipio</Name><UserStyle><Name>municipio</Name><FeatureTypeStyle><Rule><Name>A rule</Name><Title>This is a rule</Title><ns1:Filter><ns1:And><ns1:PropertyIsLessThanOrEqualTo><ns1:PropertyName>area</ns1:PropertyName><ns1:Literal>4</ns1:Literal></ns1:PropertyIsLessThanOrEqualTo><ns1:PropertyIsGreaterThanOrEqualTo><ns1:PropertyName>area</ns1:PropertyName><ns1:Literal>3</ns1:Literal></ns1:PropertyIsGreaterThanOrEqualTo></ns1:And></ns1:Filter><PolygonSymbolizer><Fill><CssParameter name="fill">#000000</CssParameter></Fill><Stroke><CssParameter name="stroke">#000000</CssParameter><CssParameter name="stroke-width">0.25</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke></PolygonSymbolizer></Rule></FeatureTypeStyle></UserStyle></NamedLayer></ns0:StyledLayerDescriptor>"""

