#!/usr/bin/env python
# coding=UTF-8

import geoserverapirest.ext.sld.ranges as sld
reload(sld)

"""
Requires the Docker-Compose to be up.

THIS TESTS ARE MEANT TO BE RUN INSIDE THE PYTHON-TEST CONTAINER OF THE DOCKER COMPOSE.
"""

class TestExtSldRanges:
    """
    ext SLD ranges test suite.
    """

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
        
        
