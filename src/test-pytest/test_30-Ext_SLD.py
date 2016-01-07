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
        self.sld = sld.GsSld()
                           

    def test_equalInterval(self):
        """
        Test equal interval output.
        """

        assert self.sld.equalInterval(1, 15, 4, 2)== \
            [[1.0, 4.49], [4.5, 7.99], [8.0, 11.49], [11.5, 15]]
        
