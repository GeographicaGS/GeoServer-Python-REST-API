#!/usr/bin/env python
# coding=UTF-8

# import geoserverapirest.core as gs
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
        "median": "",
        "high": "#4a4140"}
}


styles = {
    "test_automate_00": {
        "segmentationType": "quartile",
        "colorScheme": colorSchemes["design-seeds-color-arrange"],
        "intervals": 8,
        "precision": 1,
        "schema": "data",
        "table": "municipio",
        "column": "area",
        "dualRuleTitles": "Entre %s y %s km2",
        "monoRuleTitles": "%s km2",
        "ruleTitleLambda": lambda x: int(round(x/1000000))}
}


class TestAutomation(object):
    """
    Automation tests.
    """

    # def setup(self):
    #     pass

        
    def test_automateStyles(self):
        helpers.automateStyles(geoserver, postgis, styles)
        
