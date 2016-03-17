#!/usr/bin/env python
# coding=UTF-8

import geoserverapirest.ext.sld.color as sld
reload(sld)

"""
Requires the Docker-Compose to be up.

THIS TESTS ARE MEANT TO BE RUN INSIDE THE PYTHON-TEST CONTAINER OF THE DOCKER COMPOSE.
"""

class TestExtSldColor:
    """
    ext SLD color test suite.
    """
        
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
