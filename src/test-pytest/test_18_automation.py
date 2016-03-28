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
municipioArea = {
    "class": pg.PostGisDataSource,
    "postgis": postgis,
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
    "steps": 5,
    "low": "#dedece",
    "high": "#4a4140"
}

# A polygon automatic double ramp
polygonDoubleRamp = {
    "class": sld.SemiologyPolygonDoubleRamp,
    "stroke": stroke,
    "sidesteps": 2,
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

ConditionGtoe = {
    "class": sld.ConditionGtoe,
    "attribute": "area",
    "value": 20000000
}

ConditionEqual = {
    "class": sld.ConditionEqual,
    "attribute": "area",
    "value": "Córdoba"
}
    

# ----------------
# Styles definitions
# ----------------

# Simple, custom, single rule style

test_custom_single_rule_polygon = {
    "class": sld.StyleCustom,
    "namedlayername": "NamedLayerName",
    "stylename": "StyleName",
    "rules": ["A single rule with a stroke"],
    "filters": [None],
    "symbols": [stroke]
}

# Custom style with a couple of rules

# test_custom_dual_rule_polygon = {
#     "class": sld.StyleCustom,
#     "namedlayername": "NamedLayerName",
#     "stylename": "StyleName",
#     "rules": ["Municipios grandes Córdoba", "Municipios grandes Sevilla"],
#     "filters": [{"class": sld.FilterAnd, "c0": {"class": sld.FilterGtoe, "attribute": "area", "value": 20000000},
#                 "c1": {"class": sld.FilterEqual, "attribute": "PROVINCIA", "value": "Córdoba"}},
#                 {"class": sld.FilterAnd, "c0": {"class": sld.FilterGtoe, "attribute": "area", "value": 20000000},
#                  "c1": {"class": sld.FilterEqual, "attribute": "PROVINCIA", "value": "Sevilla"}}],
#     "symbols": [fillGreen, fillBlue]
# }

# # Automatic simple ramp with 4 steps

# area_km_rulenames = {
#     "dual": "Área entre %s y %s km2",
#     "mono": "%s km2",
#     "lambda": lambda x: int(round(x/1000000))
# }

# test_simple_ramp = {
#     "class": sld.styleSimpleIntervals,
#     "namedlayername": "NamedLayerName",
#     "stylename": "StyleName",
#     "datasource": municipioAreaSorted,
#     "intervals": 3,
#     "precision": 1,
#     "ramp": polygonSimpleRamp,
#     "ruleNames": area_km_rulenames
# }

# # Automatic double ramp with 3 sidesteps

# test_double_ramp = {
#     "class": sld.styleCenteredIntervals,
#     "namedlayername": "NamedLayerName",
#     "stylename": "StyleName",
#     "datasource": municipioAreaSorted,
#     "intervals": 3,
#     "mediandata": 32002823.98,
#     "precision": 1,
#     "ramp": polygonDoubleRamp,
#     "ruleNames": area_km_rulenames
# }


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

        ramp = sld.SemiologyPolygonSimpleRamp(polygonSimpleRamp)()
            
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

        ramp = sld.SemiologyPolygonDoubleRamp(polygonDoubleRamp)()
        
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
        
        assert pg.PostGisDataSource(municipioArea)() == test_data.rSorted
        assert pg.PostGisDataSource(municipioSmall)() == test_data.sql


    def test_ConditionGtoe(self):
        """
        Filter GTOE testing.
        """

        
                

    def test_StyleCustom(self):
        """
        StyleCustom testing.
        """

        sld.StyleCustom(test_custom_single_rule_polygon)

        sld.StyleCustom(test_custom_dual_rule_polygon)
