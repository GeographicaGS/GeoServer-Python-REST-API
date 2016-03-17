#!/usr/bin/env python
# coding=UTF-8

import geoserverapirest.ext.sld.sld as sld

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
#    "class": sld.SemiologyPolygonSimpleRamp,
    "stroke": stroke,
    "low": "#dedece",
    "high": "#4a4140"
}

# A polygon automatic double ramp
polygonDoubleRamp = {
#    "class": sld.SemiologyPolygonDoubleRamp,
    "stroke": stroke,
    "low": "#ff0000",
    "middle": "#ffffff",
    "high": "#0000ff"
}

# A polygon custom ramp
polygonCustomRamp = {
#    "class": sld.SemiologyPolygonCustomRamp,
    "stroke": stroke,
    "colors": ["#ff0000", "#00ff00", "#0000ff"]
}

# A PostGIS table data source
municipioAreaSorted = {
#    "class": pg.DataPostGisTable,
    "postgis": postgis,
    "schema": "data",
    "table": "municipio",
    "column": "area",
    "sort": True,
    "reverse": False,
    "distinct": False
}

# Style definitions
styles = {
    "test_custom_polygon": {
        "class": sld.StyleSld,
        "namedLayerName": "NamedLayerName",
        "styleName": "StyleName",
        # This three lists must be coincident in length
        "rules": ["A single rule with a stroke"],
        "filters": [None],
        "symbols": [stroke]
    }
}


# TODO: HERE continue creating and implementing examples of serialized styles
    
    # "test_custom_intervals": {
    #     "class": StyleCustomIntervals
       


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
                


                
    def test_GenerateStyles(self):
        for k,i in styles.iteritems():
            print k, i
            print
            print
            i["class"](i)
