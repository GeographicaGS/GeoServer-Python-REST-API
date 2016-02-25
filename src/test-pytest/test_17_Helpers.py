#!/usr/bin/env python
# coding=UTF-8

import geoserverapirest.core as gs
reload(gs)
import geoserverapirest.ext.helpers as helpers
reload(helpers)

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


colorSchemes = {
    "design-seeds-color-arrange": {
        "low": "#dedece",
        "high": "#4a4140"},
    "design-seeds-flora-hues": {
        "high": "#d0d4ae",
        "low": "#e9e1f2"},
    "design-seeds-color-logged": {
        "low": "#d4bfac",
        "high": "#4d413b"}
}


styles = {

    # A quartile style, with a single ramp style

    "test_automate_00": {
        "segmentationType": "quartile",
        "colorScheme": colorSchemes["design-seeds-color-arrange"],
        "intervals": 8,
        "precision": 1,
        "postgis": postgis,
        "schema": "data",
        "table": "municipio",
        "column": "area",
        "dualRuleTitles": "Entre %s y %s km2",
        "monoRuleTitles": "%s km2",
        "ruleTitleLambda": lambda x: int(round(x/1000000))},

    # A Jenks style, with a single ramp style
        
    "test_automate_01": {
        "segmentationType": "jenks",
        "colorScheme": colorSchemes["design-seeds-flora-hues"],
        "intervals": 4,
        "precision": 2,
        "postgis": postgis,
        "schema": "data",
        "table": "municipio",
        "column": "area",
        "dualRuleTitles": "Entre %s y %s ha",
        "monoRuleTitles": "%s ha",
        "ruleTitleLambda": lambda x: round(x/10000,2)},
        
    # An equal style, with a single ramp style
        
    "test_automate_02": {
        "segmentationType": "equal",
        "colorScheme": colorSchemes["design-seeds-color-logged"],
        "intervals": 5,
        "precision": 2,
        "postgis": postgis,
        "schema": "data",
        "table": "municipio",
        "column": "area",
        "dualRuleTitles": "Entre %s y %s ha",
        "monoRuleTitles": "%s ha",
        "ruleTitleLambda": lambda x: round(x/10000,2)}        
}


layers = {

    # A layer based on an SQL

    "municipio_automate_test_00": {
        "type": "sql",
        "workspace": "new_workspace",
        "datastore": "new_postgis_ds",
        "styles": ["test_automate_00", "test_automate_02"],
        "postgis": postgis,
        "sql": "select gid, \"MUNICIPIO\", area, geom from data.municipio",
        "idcolumn": "gid",
        "geomcolumn": "geom",
        "title": "Municipio layer created automatically by helpers."},

    # A layer based on a table. Keep in mind that the table's schema is provided by
    # the datastore
        
    "municipio_automate_test_01": {
        "type": "table",
        "workspace": "new_workspace",
        "datastore": "new_postgis_ds",
        "styles": ["test_automate_01", "test_automate_02"],
        "postgis": postgis,
        "table": "municipio",
        "geomcolumn": "geom",
        "title": "Municipio layer created automatically by helpers."}}


    
class TestAutomation(object):
    """
    Automation tests.
    """

    def setup(self):
        self.gsi = gs.GsInstance("http://sourcegeoserver:8080/geoserver", "admin", "geoserver")

        
    def test_automateStyles(self):
        helpers.automateStyles(geoserver, styles)

        existingStyles = self.gsi.getStyleNames()
        
        assert set([a in existingStyles for a in styles.keys()])=={True}
        
        

    def test_automateLayers(self):
        helpers.automateLayers(geoserver, layers)
        
        existingLayers = self.gsi.getLayerNames()
        
        assert set([a in existingLayers for a in layers.keys()])=={True}

