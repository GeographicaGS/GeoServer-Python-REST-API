#!/usr/bin/env python
# coding=UTF-8

import geoserverapirest.core as gs
reload(gs)
import geoserverapirest.ext.helpers as h
reload(h)
import test_data as td
reload(td)

"""
Requires the Docker-Compose to be up.

THIS TESTS ARE MEANT TO BE RUN INSIDE THE PYTHON-TEST CONTAINER OF THE DOCKER COMPOSE.
"""

geoserver = {
    "url": "http://sourcegeoserver:8080/geoserver",
    "user": "admin",
    "pass": "geoserver"
}
    
postgis = {
    "host": "db",
    "port": "5432",
    "db": "test_geoserver",
    "user": "postgres",
    "pass": "postgres"
}

Stroke = {
    "type": h.SemiologyStroke,
    "color": "#3e3e3e",
    "width": 2,
    "linejoin": h.strokeLineJoin["bevel"]}
        
Fill = {
    "type": h.SemiologyFill,
    "color": "#e3e2e1"}
        
PolygonManual = {
    "type": h.SemiologyPolygonManual,
    "stroke": Stroke,
    "fill": Fill}
        
PolygonSimpleRamp = {
    "type": h.SemiologyPolygonSimpleRamp,
    "stroke": Stroke,
    "low": "#dedece",
    "high": "#4a4140"}
        
PolygonDoubleRamp = {
    "type": h.SemiologyPolygonDoubleRamp,
    "stroke": Stroke,
    "low": "#ff0000",
    "middle": "#ffffff",
    "high": "#0000ff"}
        
PolygonManualRamp = {
    "type": h.SemiologyPolygonManualRamp,
    "stroke": Stroke,
    "colors": ["#ff0000", "#00ff00", "#0000ff"]}
        




# styles = {

#     # A quartile style, with a single ramp style

#     "test_automate_00": {
#         "type": helpers.StyleContinuousIntervals,
#         "data": {
#             "type": helpers.DataPostGisTable,
#             "postgis": postgis,
#             "schema": "data",
#             "table": "municipio",
#             "column": "area",
#             "sort": True,
#             "reverse": False,
#             "distinct": False},
#         "segmentation": {
#             "type": helpers.SegmentationQuartile,
#             "intervals": 8,
#             "precision": 4,
#             "dualRuleTitles": "Entre %s y %s km2",
#             "monoRuleTitles": "%s km2",
#             "ruleTitleLambda": lambda x: int(round(x/1000000))},
#         "semiology": {
#             "type": helpers.SemiologySimpleRamp,
#             "low": "#dedece",
#             "high": "#4a4140"}
#     },

#     "test_manual": {
#         "type": helpers.StyleManualIntervals,
#         "segmentation": {
#             "intervals": [[0,1], [1.1, 2], [2.1, 5], [5.1, 10]],
#             "dualRuleTitles": "Entre %s y %s km2",
#             "monoRuleTitles": "%s km2",
#             "ruleTitleLambda": lambda x: int(round(x/1000000))},
#         "semiology": {
#             "type": helpers.SemiologySimpleRamp,
#             "low": "#dedece",
#             "high": "#4a4140"}
#     }

# }


class TestAutomationClasses(object):
    """
    Automation classes test.
    """

    def setup(self):
        pass


    def test_SemiologyStroke(self):
        """
        Test semiology class for stroke semiology.
        """
        
        assert str(h.SemiologyStroke(Stroke)())=="""<?xml version='1.0' encoding='UTF-8'?>\n<Stroke><CssParameter name="stroke">#3e3e3e</CssParameter><CssParameter name="stroke-width">2</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke>"""


    def test_SemiologyFill(self):
        """
        Test semiology class for fill semiology.
        """

        assert str(h.SemiologyFill(Fill)())=="""<?xml version='1.0' encoding='UTF-8'?>\n<Fill><CssParameter name="fill">#e3e2e1</CssParameter></Fill>"""


    def test_SemiologyPolygonManual(self):
        """
        Test semiology class for manual polygon.
        """

        assert str(h.SemiologyPolygonManual(PolygonManual)())=="""<?xml version='1.0' encoding='UTF-8'?>\n<PolygonSymbolizer><Stroke><CssParameter name="stroke">#3e3e3e</CssParameter><CssParameter name="stroke-width">2</CssParameter><CssParameter name="stroke-linejoin">bevel</CssParameter></Stroke><Fill><CssParameter name="fill">#e3e2e1</CssParameter></Fill></PolygonSymbolizer>"""
        

            
    # def test_DataPostGisTable(self):
    #     params = {
    #         "type": helpers.DataPostGisTable,
    #         "postgis": postgis,
    #         "schema": "data",
    #         "table": "municipio",
    #         "column": "area",
    #         "sort": True,
    #         "reverse": False,
    #         "distinct": False}

            
    #     e = helpers.DataPostGisTable(params)

    #     assert e()==td.rSorted
        
            
    # def test_SegmentationQuartile(self):
    #     data = {
    #         "type": helpers.DataPostGisTable,
    #         "postgis": postgis,
    #         "schema": "data",
    #         "table": "municipio",
    #         "column": "area",
    #         "sort": True,
    #         "reverse": False,
    #         "distinct": False}
        
    #     params = {
    #         "type": helpers.SegmentationQuartile,
    #         "intervals": 8,
    #         "precision": 4,
    #         "dualRuleTitles": "Entre %s y %s km2",
    #         "monoRuleTitles": "%s km2",
    #         "ruleTitleLambda": lambda x: int(round(x/1000000))}

    #     data = helpers.DataPostGisTable(data)()
            
    #     assert helpers.SegmentationQuartile(params, data)()==[[1647885.88, 16603374.25], [16715782.5, 27553127.99], [28111989.57, 43937739.87], [44066039.62, 63533671.7], [63596281.15, 90643539.07], [90871291.25, 138495526.7], [139596745.85, 225467073.89], [225959423.09, 1254911103.14]]


    
    # "test_automate_00": {
    #     "segmentationType": "quartile",
    #     "colorScheme": colorSchemes["design-seeds-color-arrange"],
    #     "intervals": 8,
    #     "precision": 1,
    #     "postgis": postgis,
    #     "schema": "data",
    #     "table": "municipio",
    #     "column": "area",
    #     "dualRuleTitles": "Entre %s y %s km2",
    #     "monoRuleTitles": "%s km2",
    #     "ruleTitleLambda": lambda x: int(round(x/1000000))},

#     # A Jenks style, with a single ramp style
        
#     "test_automate_01": {
#         "segmentationType": "jenks",
#         "colorScheme": colorSchemes["design-seeds-flora-hues"],
#         "intervals": 4,
#         "precision": 2,
#         "postgis": postgis,
#         "schema": "data",
#         "table": "municipio",
#         "column": "area",
#         "dualRuleTitles": "Entre %s y %s ha",
#         "monoRuleTitles": "%s ha",
#         "ruleTitleLambda": lambda x: round(x/10000,2)},
        
#     # An equal style, with a single ramp style
        
#     "test_automate_02": {
#         "segmentationType": "equal",
#         "colorScheme": colorSchemes["design-seeds-color-logged"],
#         "intervals": 5,
#         "precision": 2,
#         "postgis": postgis,
#         "schema": "data",
#         "table": "municipio",
#         "column": "area",
#         "dualRuleTitles": "Entre %s y %s ha",
#         "monoRuleTitles": "%s ha",
#         "ruleTitleLambda": lambda x: round(x/10000,2)}        
# }


# layers = {

#     # A layer based on an SQL

#     "municipio_automate_test_00": {
#         "type": "sql",
#         "workspace": "new_workspace",
#         "datastore": "new_postgis_ds",
#         "styles": ["test_automate_00", "test_automate_02"],
#         "postgis": postgis,
#         "sql": "select gid, \"MUNICIPIO\", area, geom from data.municipio",
#         "idcolumn": "gid",
#         "geomcolumn": "geom",
#         "title": "Municipio layer created automatically by helpers."},

#     # A layer based on a table. Keep in mind that the table's schema is provided by
#     # the datastore
        
#     "municipio_automate_test_01": {
#         "type": "table",
#         "workspace": "new_workspace",
#         "datastore": "new_postgis_ds",
#         "styles": ["test_automate_01", "test_automate_02"],
#         "postgis": postgis,
#         "table": "municipio",
#         "geomcolumn": "geom",
#         "title": "Municipio layer created automatically by helpers."}}


    
class TestAutomation(object):
    """
    Automation tests.
    """

    def setup(self):
        self.gsi = gs.GsInstance("http://sourcegeoserver:8080/geoserver", "admin", "geoserver")

        
    # def test_automateStyles(self):
    #     h.automateStyles(geoserver, styles)

    #     existingStyles = self.gsi.getStyleNames()
        
    #     # assert set([a in existingStyles for a in styles.keys()])=={True}
        
        

    # def test_automateLayers(self):
    #     helpers.automateLayers(geoserver, layers)
        
    #     existingLayers = self.gsi.getLayerNames()
        
    #     assert set([a in existingLayers for a in layers.keys()])=={True}

