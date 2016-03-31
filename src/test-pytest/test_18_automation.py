#!/usr/bin/env python
# coding=UTF-8

import geoserverapirest.ext.sld.sld as sld
import geoserverapirest.ext.postgis.postgis as pg
import test_data

# ----------------
# Basic objects
# ----------------

# A GeoServer instance connection
geoserver = {
    "url": "http://sourcegeoserver:8080/geoserver",
    "user": "admin",
    "pass": "geoserver"
}

# A PostGIS connection
postgis = {
    "host": "db",
    "port": "5432",
    "db": "test_geoserver",
    "user": "postgres",
    "pass": "postgres"
}

# A PostGIS table data source
municipioAreaSorted = {
    "class": pg.PostGisDataSource,
    "postgis": postgis,
    "attributename": "area",
    "source": {
        "schema": "data",
        "table": "municipio",
        "column": "area",
        "sort": True,
        "reverse": False,
        "distinct": False}
}

# A PostGIS SQL data source
municipioSmall = {
    "class": pg.PostGisDataSource,
    "postgis": postgis,
    "attributename": "area",
    "source": {
        "sql": "select area from data.municipio where area<5000000 order by area"
    }
}
    

# ----------------
# SLD definitions
# ----------------

colors = {
    "green": "#3C7113",
    "blue": "#113B51"
}

# A stroke symbol
stroke = {
    "class": sld.SemiologyStroke,
    "color": "#3e3e3e",
    "width": 2,
    "linejoin": sld.strokeLineJoin["bevel"]
}

# A fill symbol
fill = {
    "class": sld.SemiologyFill,
    "color": "#e3e2e1"
}

# A green fill symbol
fillGreen = {
    "class": sld.SemiologyFill,
    "color": colors["green"],
    "stroke": stroke
}

# A blue fill symbol
fillBlue = {
    "class": sld.SemiologyFill,
    "color": colors["blue"],
    "stroke": stroke    
}
        
# A polygon symbol with stroke and fill
polygonStrokeFill = {
    "class": sld.SemiologyPolygon,
    "stroke": stroke,
    "fill": fill
}

# A polygon symbol with only fill
polygonFill = {
    "class": sld.SemiologyPolygon,
    "fill": fill
}

# A polygon symbol with only stroke
polygonStroke = {
    "class": sld.SemiologyPolygon,
    "stroke": stroke
}

# A polygon automatic simple ramp
polygonSimpleRamp = {
    "class": sld.SemiologyPolygonSimpleRamp,
    "stroke": stroke,
    "low": "#dedece",
    "high": "#4a4140"
}

# A polygon automatic double ramp
polygonDoubleRamp = {
    "class": sld.SemiologyPolygonDoubleRamp,
    "stroke": stroke,
    "low": "#ff0000",
    "middle": "#ffffff",
    "high": "#0000ff"
}

# A polygon custom ramp
polygonCustomRamp = {
    "class": sld.SemiologyPolygonCustomRamp,
    "stroke": stroke,
    "colors": ["#ff0000", "#00ff00", "#0000ff"]
}


# ----------------
# Condition definitions
# ----------------

conditionGtoe = {
    "class": sld.ConditionGtoe,
    "attribute": "area",
    "value": 400000000
}

conditionLtoe = {
    "class": sld.ConditionLtoe,
    "attribute": "area",
    "value": 400000000
}

conditionEqual = {
    "class": sld.ConditionEqual,
    "attribute": "PROVINCIA",
    "value": "Córdoba"
}

conditionAnd = {
    "class": sld.ConditionAnd,
    "c0": conditionLtoe,
    "c1": conditionEqual
}

conditionOr = {
    "class": sld.ConditionAnd,
    "c0": conditionAnd,
    "c1": conditionEqual
}

endOfWorldCondition = {
    "class": sld.ConditionAnd,
    "c0": conditionAnd,
    "c1": conditionOr
}
        

# -----------------------
# Full styles definitions
# -----------------------

# Simple, custom, single rule style

test_custom_single_rule_polygon = {
    "class": sld.StyleCustom,
    "namedlayername": "NamedLayerName",
    "stylename": "StyleName",
    "rulenames": ["A single rule with a stroke"],
    "symbols": [polygonStroke]
}

# Single filter

test_custom_single_filter_polygon = {
    "class": sld.StyleCustom,
    "namedlayername": "NamedLayerName",
    "stylename": "StyleName",
    "rulenames": ["Municipios grandes"],
    "conditions": [{"class": sld.ConditionGtoe, "attribute": "area", "value": 400000000}],
    "symbols": [polygonStroke]
}
    
# Custom style with a couple of rules

test_custom_dual_rule_polygon = {
    "class": sld.StyleCustom,
    "namedlayername": "NamedLayerName",
    "stylename": "StyleName",
    "rulenames": ["Municipios grandes Córdoba", "Municipios grandes Sevilla"],
    "conditions": [{"class": sld.ConditionAnd, "c0": {"class": sld.ConditionGtoe, "attribute": "area", "value": 400000000},
                "c1": {"class": sld.ConditionEqual, "attribute": "PROVINCIA", "value": "Córdoba"}},
                {"class": sld.ConditionAnd, "c0": {"class": sld.ConditionGtoe, "attribute": "area", "value": 400000000},
                 "c1": {"class": sld.ConditionEqual, "attribute": "PROVINCIA", "value": "Sevilla"}}],
    "symbols": [{"class": sld.SemiologyPolygon, "fill": fillBlue}, {"class": sld.SemiologyPolygon, "fill": fillGreen}]
}

# Automatic simple ramp with 4 steps

area_km_rulenames = {
    "dual": "Área entre %s y %s km2",
    "mono": "%s km2",
    "lambda": lambda x: int(round(x/1000000))
}

test_simple_ramp = {
    "class": sld.StyleSimpleIntervals,
    "namedlayername": "NamedLayerName",
    "stylename": "StyleName",
    "datasource": municipioAreaSorted,
    "rangetype": sld.RangesEqual,
    "steps": 3,
    "precision": 3,
    "ramp": polygonSimpleRamp,
    "rulenames": area_km_rulenames
}

# Automatic double ramp with 3 sidesteps

test_double_ramp = {
    "class": sld.StyleCenteredIntervals,
    "namedlayername": "NamedLayerName",
    "stylename": "StyleName",
    "datasource": municipioAreaSorted,
    "rangetype": sld.RangesQuartile,
    "steps": 2,
    "mediandata": 150220197.13,
    "precision": 3,
    "ramp": polygonDoubleRamp,
    "rulenames": area_km_rulenames
}


class TestAutomationClasses(object):
    """
    Automation classes testing.
    """

    def test_SemiologyStroke(self):
        """
        SemiologyStroke testing.
        """

        assert str(sld.SemiologyStroke(stroke)())=="""<?xml version='1.0' encoding='UTF-8'?>\n<Stroke><CssParameter name="stroke">#3e3e3e</CssParameter><CssParameter name="stroke-width">2</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke>"""

        
    def test_SemiologyFill(self):
        """
        SemiologyFill testing.
        """

        assert str(sld.SemiologyFill(fill)())=="""<?xml version='1.0' encoding='UTF-8'?>\n<Fill><CssParameter name="fill">#e3e2e1</CssParameter></Fill>"""


    def test_SemiologyPolygon(self):
        """
        SemiologyPolygon testing.
        """

        assert str(sld.SemiologyPolygon(polygonStrokeFill)())=="""<?xml version='1.0' encoding='UTF-8'?>\n<PolygonSymbolizer><Stroke><CssParameter name="stroke">#3e3e3e</CssParameter><CssParameter name="stroke-width">2</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke><Fill><CssParameter name="fill">#e3e2e1</CssParameter></Fill></PolygonSymbolizer>"""

        assert str(sld.SemiologyPolygon(polygonStroke)())=="""<?xml version='1.0' encoding='UTF-8'?>\n<PolygonSymbolizer><Stroke><CssParameter name="stroke">#3e3e3e</CssParameter><CssParameter name="stroke-width">2</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke></PolygonSymbolizer>"""

        assert str(sld.SemiologyPolygon(polygonFill)())=="""<?xml version='1.0' encoding='UTF-8'?>\n<PolygonSymbolizer><Fill><CssParameter name="fill">#e3e2e1</CssParameter></Fill></PolygonSymbolizer>"""
                

    def test_SemiologyPolygonSimpleRamp(self):
        """
        SemiologyPolygonSimpleRamp testing.
        """

        solutions = [
            """<?xml version='1.0' encoding='UTF-8'?>\n<PolygonSymbolizer><Stroke><CssParameter name="stroke">#3e3e3e</CssParameter><CssParameter name="stroke-width">2</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke><Fill><CssParameter name="fill">#dedece</CssParameter></Fill></PolygonSymbolizer>""",
            """<?xml version='1.0' encoding='UTF-8'?>\n<PolygonSymbolizer><Stroke><CssParameter name="stroke">#3e3e3e</CssParameter><CssParameter name="stroke-width">2</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke><Fill><CssParameter name="fill">#beb9a5</CssParameter></Fill></PolygonSymbolizer>""",
            """<?xml version='1.0' encoding='UTF-8'?>\n<PolygonSymbolizer><Stroke><CssParameter name="stroke">#3e3e3e</CssParameter><CssParameter name="stroke-width">2</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke><Fill><CssParameter name="fill">#9d8f7e</CssParameter></Fill></PolygonSymbolizer>""",
            """<?xml version='1.0' encoding='UTF-8'?>\n<PolygonSymbolizer><Stroke><CssParameter name="stroke">#3e3e3e</CssParameter><CssParameter name="stroke-width">2</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke><Fill><CssParameter name="fill">#74655e</CssParameter></Fill></PolygonSymbolizer>""",
            """<?xml version='1.0' encoding='UTF-8'?>\n<PolygonSymbolizer><Stroke><CssParameter name="stroke">#3e3e3e</CssParameter><CssParameter name="stroke-width">2</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke><Fill><CssParameter name="fill">#4a4140</CssParameter></Fill></PolygonSymbolizer>"""]

        ramp = sld.SemiologyPolygonSimpleRamp(polygonSimpleRamp, 5)()
            
        for a in range(0, len(ramp)):
            assert str(ramp[a])==solutions[a]


    def test_SemiologyPolygonDoubleRamp(self):
        """
        SemiologyPolygonDoubleRamp testing.
        """

        solutions = [
            """<?xml version='1.0' encoding='UTF-8'?>\n<PolygonSymbolizer><Stroke><CssParameter name="stroke">#3e3e3e</CssParameter><CssParameter name="stroke-width">2</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke><Fill><CssParameter name="fill">#ff0000</CssParameter></Fill></PolygonSymbolizer>""",
            """<?xml version='1.0' encoding='UTF-8'?>\n<PolygonSymbolizer><Stroke><CssParameter name="stroke">#3e3e3e</CssParameter><CssParameter name="stroke-width">2</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke><Fill><CssParameter name="fill">#df9f9f</CssParameter></Fill></PolygonSymbolizer>""",
            """<?xml version='1.0' encoding='UTF-8'?>\n<PolygonSymbolizer><Stroke><CssParameter name="stroke">#3e3e3e</CssParameter><CssParameter name="stroke-width">2</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke><Fill><CssParameter name="fill">#ffffff</CssParameter></Fill></PolygonSymbolizer>""",
            """<?xml version='1.0' encoding='UTF-8'?>\n<PolygonSymbolizer><Stroke><CssParameter name="stroke">#3e3e3e</CssParameter><CssParameter name="stroke-width">2</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke><Fill><CssParameter name="fill">#9fdf9f</CssParameter></Fill></PolygonSymbolizer>""",
            """<?xml version='1.0' encoding='UTF-8'?>\n<PolygonSymbolizer><Stroke><CssParameter name="stroke">#3e3e3e</CssParameter><CssParameter name="stroke-width">2</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke><Fill><CssParameter name="fill">#0000ff</CssParameter></Fill></PolygonSymbolizer>"""]

        ramp = sld.SemiologyPolygonDoubleRamp(polygonDoubleRamp, 2)()
        
        for a in range(0, len(ramp)):
            assert str(ramp[a])==solutions[a]


    def test_SemiologyPolygonCustomRamp(self):
        """
        SemiologyPolygonCustomRamp testing.
        """

        solutions = [
            """<?xml version='1.0' encoding='UTF-8'?>\n<PolygonSymbolizer><Stroke><CssParameter name="stroke">#3e3e3e</CssParameter><CssParameter name="stroke-width">2</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke><Fill><CssParameter name="fill">#ff0000</CssParameter></Fill></PolygonSymbolizer>""",
            """<?xml version='1.0' encoding='UTF-8'?>\n<PolygonSymbolizer><Stroke><CssParameter name="stroke">#3e3e3e</CssParameter><CssParameter name="stroke-width">2</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke><Fill><CssParameter name="fill">#00ff00</CssParameter></Fill></PolygonSymbolizer>""",
            """<?xml version='1.0' encoding='UTF-8'?>\n<PolygonSymbolizer><Stroke><CssParameter name="stroke">#3e3e3e</CssParameter><CssParameter name="stroke-width">2</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke><Fill><CssParameter name="fill">#0000ff</CssParameter></Fill></PolygonSymbolizer>"""]

        ramp = sld.SemiologyPolygonCustomRamp(polygonCustomRamp)()
        
        for a in range(0, len(ramp)):
            assert str(ramp[a])==solutions[a]


    def test_PostGisDataSource(self):
        """
        DataPostGisTable testing.
        """
        
        assert pg.PostGisDataSource(municipioAreaSorted)() == test_data.rSorted
        assert pg.PostGisDataSource(municipioSmall)() == test_data.sql


    def test_ConditionGtoe(self):
        """
        Condition GTOE testing.
        """

        assert str(sld.ConditionGtoe(conditionGtoe)()) == """<?xml version='1.0' encoding='UTF-8'?>\n<ns0:PropertyIsGreaterThanOrEqualTo xmlns:ns0="http://www.opengis.net/ogc"><ns0:PropertyName>area</ns0:PropertyName><ns0:Literal>400000000</ns0:Literal></ns0:PropertyIsGreaterThanOrEqualTo>"""
        

    def test_ConditionLtoe(self):
        """
        Condition LTOE testing.
        """

        assert str(sld.ConditionLtoe(conditionLtoe)()) == """<?xml version='1.0' encoding='UTF-8'?>\n<ns0:PropertyIsLessThanOrEqualTo xmlns:ns0="http://www.opengis.net/ogc"><ns0:PropertyName>area</ns0:PropertyName><ns0:Literal>400000000</ns0:Literal></ns0:PropertyIsLessThanOrEqualTo>"""


    def test_ConditionEqual(self):
        """
        Condition EQUAL testing.
        """

        assert str(sld.ConditionEqual(conditionEqual)()) == """<?xml version='1.0' encoding='UTF-8'?>\n<ns0:PropertyIsEqualTo xmlns:ns0="http://www.opengis.net/ogc"><ns0:PropertyName>PROVINCIA</ns0:PropertyName><ns0:Literal>Córdoba</ns0:Literal></ns0:PropertyIsEqualTo>"""


    def test_ConditionAnd(self):
        """
        Condition AND testing.
        """

        assert str(sld.ConditionAnd(conditionAnd)()) == """<?xml version='1.0' encoding='UTF-8'?>\n<ns0:And xmlns:ns0="http://www.opengis.net/ogc"><ns0:PropertyIsEqualTo><ns0:PropertyName>PROVINCIA</ns0:PropertyName><ns0:Literal>Córdoba</ns0:Literal></ns0:PropertyIsEqualTo><ns0:PropertyIsLessThanOrEqualTo><ns0:PropertyName>area</ns0:PropertyName><ns0:Literal>400000000</ns0:Literal></ns0:PropertyIsLessThanOrEqualTo></ns0:And>"""


    def test_ConditionOr(self):
        """
        Condition OR testing.
        """

        assert str(sld.ConditionOr(conditionOr)()) == """<?xml version='1.0' encoding='UTF-8'?>\n<ns0:Or xmlns:ns0="http://www.opengis.net/ogc"><ns0:PropertyIsEqualTo><ns0:PropertyName>PROVINCIA</ns0:PropertyName><ns0:Literal>Córdoba</ns0:Literal></ns0:PropertyIsEqualTo><ns0:And><ns0:PropertyIsEqualTo><ns0:PropertyName>PROVINCIA</ns0:PropertyName><ns0:Literal>Córdoba</ns0:Literal></ns0:PropertyIsEqualTo><ns0:PropertyIsLessThanOrEqualTo><ns0:PropertyName>area</ns0:PropertyName><ns0:Literal>400000000</ns0:Literal></ns0:PropertyIsLessThanOrEqualTo></ns0:And></ns0:Or>"""
        

    def test_endOfWorldCondition(self):
        """
        Complex condition.
        """

        assert str(endOfWorldCondition["class"](endOfWorldCondition)()) == """<?xml version='1.0' encoding='UTF-8'?>\n<ns0:And xmlns:ns0="http://www.opengis.net/ogc"><ns0:And><ns0:PropertyIsEqualTo><ns0:PropertyName>PROVINCIA</ns0:PropertyName><ns0:Literal>Córdoba</ns0:Literal></ns0:PropertyIsEqualTo><ns0:And><ns0:PropertyIsEqualTo><ns0:PropertyName>PROVINCIA</ns0:PropertyName><ns0:Literal>Córdoba</ns0:Literal></ns0:PropertyIsEqualTo><ns0:PropertyIsLessThanOrEqualTo><ns0:PropertyName>area</ns0:PropertyName><ns0:Literal>400000000</ns0:Literal></ns0:PropertyIsLessThanOrEqualTo></ns0:And></ns0:And><ns0:And><ns0:PropertyIsEqualTo><ns0:PropertyName>PROVINCIA</ns0:PropertyName><ns0:Literal>Córdoba</ns0:Literal></ns0:PropertyIsEqualTo><ns0:PropertyIsLessThanOrEqualTo><ns0:PropertyName>area</ns0:PropertyName><ns0:Literal>400000000</ns0:Literal></ns0:PropertyIsLessThanOrEqualTo></ns0:And></ns0:And>"""


    # --------------
    # Ranges testing
    # --------------

    def test_range_quartile_testing(self):
        """
        Testing ranges.
        """

        assert sld.RangesQuartile(pg.PostGisDataSource(municipioAreaSorted)(), 3, 1)()== \
          [[1647885.88, 38810191.13], [39034687.58, 103034890.49], [103474124.71, 1254911103.14]]

        assert sld.RangesEqual(pg.PostGisDataSource(municipioAreaSorted)(), 3, 1)()== \
          [[1647885.9, 419402291.6], [419402291.7, 837156697.4], [837156697.5, 1254911103.14]]

        assert sld.RangesJenksMiddle(pg.PostGisDataSource(municipioAreaSorted)(), 2, 400000000, 1)()== \
          [[1647885.9, 134211289.0], [135510494.7, 395894511.5], [400000000, 400000000], \
           [403658688.7, 749134072.1], [860616884.5, 1254911103.1]]

        # Jenks is not tested because of its variability
          
    # ------------
    # Full style testing
    # ------------
    
    def test_StyleCustom(self):
        """
        StyleCustom testing.
        """

        assert str(sld.StyleCustom(test_custom_single_rule_polygon)())=="""<?xml version='1.0' encoding='UTF-8'?>\n<ns0:StyledLayerDescriptor xmlns:ns0="http://www.opengis.net/sld" version="1.0.0"><NamedLayer><Name>NamedLayerName</Name><UserStyle><Name>StyleName</Name><FeatureTypeStyle><Rule><Name>a_single_rule_with_a_stroke</Name><Title>A single rule with a stroke</Title><PolygonSymbolizer><Stroke><CssParameter name="stroke">#3e3e3e</CssParameter><CssParameter name="stroke-width">2</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke></PolygonSymbolizer></Rule></FeatureTypeStyle></UserStyle></NamedLayer></ns0:StyledLayerDescriptor>"""

        assert str(sld.StyleCustom(test_custom_single_filter_polygon)())=="""<?xml version='1.0' encoding='UTF-8'?>\n<ns0:StyledLayerDescriptor xmlns:ns0="http://www.opengis.net/sld" xmlns:ns1="http://www.opengis.net/ogc" version="1.0.0"><NamedLayer><Name>NamedLayerName</Name><UserStyle><Name>StyleName</Name><FeatureTypeStyle><Rule><Name>municipios_grandes</Name><Title>Municipios grandes</Title><ns1:Filter><ns1:PropertyIsGreaterThanOrEqualTo><ns1:PropertyName>area</ns1:PropertyName><ns1:Literal>400000000</ns1:Literal></ns1:PropertyIsGreaterThanOrEqualTo></ns1:Filter><PolygonSymbolizer><Stroke><CssParameter name="stroke">#3e3e3e</CssParameter><CssParameter name="stroke-width">2</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke></PolygonSymbolizer></Rule></FeatureTypeStyle></UserStyle></NamedLayer></ns0:StyledLayerDescriptor>"""

        assert str(sld.StyleCustom(test_custom_dual_rule_polygon)())=="""<?xml version='1.0' encoding='UTF-8'?>\n<ns0:StyledLayerDescriptor xmlns:ns0="http://www.opengis.net/sld" xmlns:ns1="http://www.opengis.net/ogc" version="1.0.0"><NamedLayer><Name>NamedLayerName</Name><UserStyle><Name>StyleName</Name><FeatureTypeStyle><Rule><Name>municipios_grandes_sevilla</Name><Title>Municipios grandes Sevilla</Title><ns1:Filter><ns1:And><ns1:PropertyIsEqualTo><ns1:PropertyName>PROVINCIA</ns1:PropertyName><ns1:Literal>Sevilla</ns1:Literal></ns1:PropertyIsEqualTo><ns1:PropertyIsGreaterThanOrEqualTo><ns1:PropertyName>area</ns1:PropertyName><ns1:Literal>400000000</ns1:Literal></ns1:PropertyIsGreaterThanOrEqualTo></ns1:And></ns1:Filter><PolygonSymbolizer><Fill><CssParameter name="fill">#3C7113</CssParameter></Fill></PolygonSymbolizer></Rule><Rule><Name>municipios_grandes_córdoba</Name><Title>Municipios grandes Córdoba</Title><ns1:Filter><ns1:And><ns1:PropertyIsEqualTo><ns1:PropertyName>PROVINCIA</ns1:PropertyName><ns1:Literal>Córdoba</ns1:Literal></ns1:PropertyIsEqualTo><ns1:PropertyIsGreaterThanOrEqualTo><ns1:PropertyName>area</ns1:PropertyName><ns1:Literal>400000000</ns1:Literal></ns1:PropertyIsGreaterThanOrEqualTo></ns1:And></ns1:Filter><PolygonSymbolizer><Fill><CssParameter name="fill">#113B51</CssParameter></Fill></PolygonSymbolizer></Rule></FeatureTypeStyle></UserStyle></NamedLayer></ns0:StyledLayerDescriptor>"""

        assert str(sld.StyleSimpleIntervals(test_simple_ramp)())=="""<?xml version='1.0' encoding='UTF-8'?>\n<ns0:StyledLayerDescriptor xmlns:ns0="http://www.opengis.net/sld" xmlns:ns1="http://www.opengis.net/ogc" version="1.0.0"><NamedLayer><Name>NamedLayerName</Name><UserStyle><Name>StyleName</Name><FeatureTypeStyle><Rule><Name>Área_entre_837_y_1255_km2</Name><Title>Área entre 837 y 1255 km2</Title><ns1:Filter><ns1:And><ns1:PropertyIsLessThanOrEqualTo><ns1:PropertyName>area</ns1:PropertyName><ns1:Literal>1254911103.14</ns1:Literal></ns1:PropertyIsLessThanOrEqualTo><ns1:PropertyIsGreaterThanOrEqualTo><ns1:PropertyName>area</ns1:PropertyName><ns1:Literal>837156697.386</ns1:Literal></ns1:PropertyIsGreaterThanOrEqualTo></ns1:And></ns1:Filter><PolygonSymbolizer><Stroke><CssParameter name="stroke">#3e3e3e</CssParameter><CssParameter name="stroke-width">2</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke><Fill><CssParameter name="fill">#4a4140</CssParameter></Fill></PolygonSymbolizer></Rule><Rule><Name>Área_entre_419_y_837_km2</Name><Title>Área entre 419 y 837 km2</Title><ns1:Filter><ns1:And><ns1:PropertyIsLessThanOrEqualTo><ns1:PropertyName>area</ns1:PropertyName><ns1:Literal>837156697.385</ns1:Literal></ns1:PropertyIsLessThanOrEqualTo><ns1:PropertyIsGreaterThanOrEqualTo><ns1:PropertyName>area</ns1:PropertyName><ns1:Literal>419402291.633</ns1:Literal></ns1:PropertyIsGreaterThanOrEqualTo></ns1:And></ns1:Filter><PolygonSymbolizer><Stroke><CssParameter name="stroke">#3e3e3e</CssParameter><CssParameter name="stroke-width">2</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke><Fill><CssParameter name="fill">#9d8f7e</CssParameter></Fill></PolygonSymbolizer></Rule><Rule><Name>Área_entre_2_y_419_km2</Name><Title>Área entre 2 y 419 km2</Title><ns1:Filter><ns1:And><ns1:PropertyIsLessThanOrEqualTo><ns1:PropertyName>area</ns1:PropertyName><ns1:Literal>419402291.632</ns1:Literal></ns1:PropertyIsLessThanOrEqualTo><ns1:PropertyIsGreaterThanOrEqualTo><ns1:PropertyName>area</ns1:PropertyName><ns1:Literal>1647885.88</ns1:Literal></ns1:PropertyIsGreaterThanOrEqualTo></ns1:And></ns1:Filter><PolygonSymbolizer><Stroke><CssParameter name="stroke">#3e3e3e</CssParameter><CssParameter name="stroke-width">2</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke><Fill><CssParameter name="fill">#dedece</CssParameter></Fill></PolygonSymbolizer></Rule></FeatureTypeStyle></UserStyle></NamedLayer></ns0:StyledLayerDescriptor>"""

        assert str(sld.StyleCenteredIntervals(test_double_ramp)())=="""<?xml version='1.0' encoding='UTF-8'?>\n<ns0:StyledLayerDescriptor xmlns:ns0="http://www.opengis.net/sld" xmlns:ns1="http://www.opengis.net/ogc" version="1.0.0"><NamedLayer><Name>NamedLayerName</Name><UserStyle><Name>StyleName</Name><FeatureTypeStyle><Rule><Name>Área_entre_243_y_1255_km2</Name><Title>Área entre 243 y 1255 km2</Title><ns1:Filter><ns1:And><ns1:PropertyIsLessThanOrEqualTo><ns1:PropertyName>area</ns1:PropertyName><ns1:Literal>1254911103.14</ns1:Literal></ns1:PropertyIsLessThanOrEqualTo><ns1:PropertyIsGreaterThanOrEqualTo><ns1:PropertyName>area</ns1:PropertyName><ns1:Literal>243060148.57</ns1:Literal></ns1:PropertyIsGreaterThanOrEqualTo></ns1:And></ns1:Filter><PolygonSymbolizer><Stroke><CssParameter name="stroke">#3e3e3e</CssParameter><CssParameter name="stroke-width">2</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke><Fill><CssParameter name="fill">#0000ff</CssParameter></Fill></PolygonSymbolizer></Rule><Rule><Name>Área_entre_151_y_239_km2</Name><Title>Área entre 151 y 239 km2</Title><ns1:Filter><ns1:And><ns1:PropertyIsLessThanOrEqualTo><ns1:PropertyName>area</ns1:PropertyName><ns1:Literal>239360830.85</ns1:Literal></ns1:PropertyIsLessThanOrEqualTo><ns1:PropertyIsGreaterThanOrEqualTo><ns1:PropertyName>area</ns1:PropertyName><ns1:Literal>150787727.06</ns1:Literal></ns1:PropertyIsGreaterThanOrEqualTo></ns1:And></ns1:Filter><PolygonSymbolizer><Stroke><CssParameter name="stroke">#3e3e3e</CssParameter><CssParameter name="stroke-width">2</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke><Fill><CssParameter name="fill">#9fdf9f</CssParameter></Fill></PolygonSymbolizer></Rule><Rule><Name>150_km2</Name><Title>150 km2</Title><ns1:Filter><ns1:And><ns1:PropertyIsLessThanOrEqualTo><ns1:PropertyName>area</ns1:PropertyName><ns1:Literal>150220197.13</ns1:Literal></ns1:PropertyIsLessThanOrEqualTo><ns1:PropertyIsGreaterThanOrEqualTo><ns1:PropertyName>area</ns1:PropertyName><ns1:Literal>150220197.13</ns1:Literal></ns1:PropertyIsGreaterThanOrEqualTo></ns1:And></ns1:Filter><PolygonSymbolizer><Stroke><CssParameter name="stroke">#3e3e3e</CssParameter><CssParameter name="stroke-width">2</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke><Fill><CssParameter name="fill">#ffffff</CssParameter></Fill></PolygonSymbolizer></Rule><Rule><Name>Área_entre_45_y_149_km2</Name><Title>Área entre 45 y 149 km2</Title><ns1:Filter><ns1:And><ns1:PropertyIsLessThanOrEqualTo><ns1:PropertyName>area</ns1:PropertyName><ns1:Literal>148765231.62</ns1:Literal></ns1:PropertyIsLessThanOrEqualTo><ns1:PropertyIsGreaterThanOrEqualTo><ns1:PropertyName>area</ns1:PropertyName><ns1:Literal>45418729.48</ns1:Literal></ns1:PropertyIsGreaterThanOrEqualTo></ns1:And></ns1:Filter><PolygonSymbolizer><Stroke><CssParameter name="stroke">#3e3e3e</CssParameter><CssParameter name="stroke-width">2</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke><Fill><CssParameter name="fill">#df9f9f</CssParameter></Fill></PolygonSymbolizer></Rule><Rule><Name>Área_entre_2_y_45_km2</Name><Title>Área entre 2 y 45 km2</Title><ns1:Filter><ns1:And><ns1:PropertyIsLessThanOrEqualTo><ns1:PropertyName>area</ns1:PropertyName><ns1:Literal>45208644.7</ns1:Literal></ns1:PropertyIsLessThanOrEqualTo><ns1:PropertyIsGreaterThanOrEqualTo><ns1:PropertyName>area</ns1:PropertyName><ns1:Literal>1647885.88</ns1:Literal></ns1:PropertyIsGreaterThanOrEqualTo></ns1:And></ns1:Filter><PolygonSymbolizer><Stroke><CssParameter name="stroke">#3e3e3e</CssParameter><CssParameter name="stroke-width">2</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke><Fill><CssParameter name="fill">#ff0000</CssParameter></Fill></PolygonSymbolizer></Rule></FeatureTypeStyle></UserStyle></NamedLayer></ns0:StyledLayerDescriptor>"""
