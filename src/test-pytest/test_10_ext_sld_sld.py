#!/usr/bin/env python
# coding=UTF-8

import geoserverapirest.ext.sld.sld as sld
reload(sld)

"""
Requires the Docker-Compose to be up.

THIS TESTS ARE MEANT TO BE RUN INSIDE THE PYTHON-TEST CONTAINER OF THE DOCKER COMPOSE.
"""


Stroke = {
    "type": sld.SemiologyStroke,
    "color": "#3e3e3e",
    "width": 2,
    "linejoin": sld.strokeLineJoin["bevel"]}


    
class TestExtSldSld:
    """
    ext SLD SLD entry point.
    """
        
