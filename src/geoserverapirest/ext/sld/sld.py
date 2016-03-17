#!/usr/bin/env python
# coding=UTF-8

import geoserverapirest.ext.sld.core as core

"""
This set of classes works as helpers to construct SLD and should be the only entry point to this module.
They are designed to work supplying dictionaries of properties so they can be used by means of defining
objects via dictionaries.
"""

strokeLineJoin = core.strokeLineJoin


class Automation(object):
    """
    Automation objects base class.

    All this classes do something in the __init__ and store the final output in the
    out variable. This out variable can be retrieved just by calling the object as
    WhateverAutomationObject().
    """
    out = None
        
    def __call__(self):
        """
        Treat self.sld() as itself.
        """
        return self.out


    
class SemiologyStroke(Automation):
    """
    Automation for stroke semiology.

    Takes a stroke specification as a dictionary and stores a sld.GsSldStrokeSymbolizer:

    stroke = {
       "class": sld.SemiologyStroke,
       "color": "#3e3e3e",
       "width": 2,
       "linejoin": strokeLineJoin["bevel"]
    }
    """

    def __init__(self, params):
        self.out = core.GsSldStrokeSymbolizer(params["color"], params["width"], params["linejoin"])



class SemiologyFill(Automation):
    """
    Automation for fill semiology.

    Takes a fill specification as a dictionary and stores a sld.GsSldFillSymbolizer:

    fill = {
       "class": sld.SemiologyFill,
       "color": "#e3e2e1"
    }
    """

    def __init__(self, params):
        self.out = core.GsSldFillSymbolizer(params["color"])



class SemiologyPolygon(Automation):
    """
    Automation for polygon semiology.

    Takes a polygon symbol specification as a dictionary and stores a sld.GsSldPolygonSymbolizer:

    polygonStrokeFill = {
        "class": sld.SemiologyPolygon,
        "stroke": stroke,
        "fill": fill
    }
    """

    def __init__(self, params):
        self.out = core.GsSldPolygonSymbolizer()

        if "stroke" in params.keys():
            self.out.addSymbol(SemiologyStroke(params["stroke"])())

        if "fill" in params.keys():
            self.out.addSymbol(SemiologyFill(params["fill"])())



class StyleSld(Automation):
    """
    Automation for a full SLD style.

    Takes a style specification as a dictionary and builds a full SLD. See test_18_automation.py for examples.


    TODO: Here, continue creating styles as per createFeatureTypeStyle at sld-deprecate.py.
    """

    def __init__(self, params):
        symbols = [a["class"](a)() for a in params["symbols"]]
        rules = [a["class"](a)() if isinstance(a, dict) else a for a in params["rules"]]
        filters = [a["class"](a)() if isinstance(a, dict) else a for a in params["filters"]]

        print
        print symbols
        print
        print rules
        print
        print filters

        for i in range(0, len(rules)):
            pass
