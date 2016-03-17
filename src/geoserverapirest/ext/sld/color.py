#!/usr/bin/env python
# coding=UTF-8

import colour

"""
Color calculations.
"""
    
class Color(object):
    """
    Color manipulation methods.
    """

    def colorRamp(self, initial, final, steps):
        """
        Returns a list with color codes between initial, final in a given steps.
        """

        e = list(colour.Color(initial).range_to(colour.Color(final), steps))

        return [i.get_hex_l() for i in e]

    
    def colorDualRamp(self, initial, middle, final, sideSteps):
        """
        Returns a list with colors with a dual ramp.
        """

        low = list(colour.Color(initial).range_to(colour.Color(middle), sideSteps+1))
        high = list(colour.Color(middle).range_to(colour.Color(final), sideSteps+1))

        low[:-1].append(middle)
        low.extend(high[1:])

        return [i.get_hex_l() for i in low]
