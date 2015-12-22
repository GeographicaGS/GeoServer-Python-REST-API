#!/usr/bin/env python
# coding=UTF-8

import math

class GsSld(object):
    """
    This class composes SLD styles.
    """

    def __init__(self):
        pass


    def equalInterval(self, min, max, intervals, precision):
        """
        Returns equal intervals.

        :param min: Lower limit of the interval.
        :type min: Float
        :param max: Upper limit of the interval.
        :type max: Float
        :param intervals: Number of intervals.
        :type intervals: Integer
        :param precision: Precision of interval limits.
        :type precision: Integer
        :return: A list of lists containing the interval limits.
        :rtype: List
        """

        step = round((max-min)*1.00/intervals, precision)
        precisionStep = math.pow(10, -precision)
        out = []
        
        for i in range(0, intervals):
            out.append([round(min+(i*step), precision),
                        round(min+((i+1)*step)-precisionStep, precision)])

        # Redefine upper from last interval
        out[-1][1] = max

        return out
        

    
