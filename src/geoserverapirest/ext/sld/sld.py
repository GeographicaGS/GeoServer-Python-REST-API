#!/usr/bin/env python
# coding=UTF-8

import geoserverapirest.ext.sld.core as core, geoserverapirest.ext.sld.color as color

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



class SemiologyPolygonSimpleRamp(Automation):
    """
    Automation for a polygon simple ramp.

    Takes a polygon simple ramp specification as a dictionary and stores a list of sld.GsSldPolygonSymbolizer:

    polygonSimpleRamp = {
        "class": sld.SemiologyPolygonSimpleRamp,
        "stroke": stroke,
        "steps": 5,        
        "low": "#dedece",
        "high": "#4a4140"
    }
    """

    def __init__(self, params):
        self.out = []

        c = color.Color()
        colors = c.colorRamp(params["low"], params["high"], params["steps"])

        for i in range(0, params["steps"]):
            o = core.GsSldPolygonSymbolizer()
            
            if "stroke" in params.keys():
                o.addSymbol(SemiologyStroke(params["stroke"])())

            o.addSymbol(SemiologyFill({"color": colors[i]})())

            self.out.append(o)



class SemiologyPolygonDoubleRamp(Automation):
    """
    Automation for a polygon double ramp.

    Takes a polygon double ramp specification as a dictionary and stores a list of sld.GsSldPolygonSymbolizer:

    polygonDoubleRamp = {
        "class": sld.SemiologyPolygonDoubleRamp,
        "stroke": stroke,
        "low": "#ff0000",
        "middle": "#ffffff",
        "high": "#0000ff"
    }
    """

    def __init__(self, params):
        self.out = []

        c = color.Color()
        colors = c.colorDualRamp(params["low"], params["middle"], params["high"], params["sidesteps"])

        for i in range(0, (params["sidesteps"]*2)+1):
            o = core.GsSldPolygonSymbolizer()

            if "stroke" in params.keys():
                o.addSymbol(SemiologyStroke(params["stroke"])())

            o.addSymbol(SemiologyFill({"color": colors[i]})())

            self.out.append(o)



class SemiologyPolygonCustomRamp(Automation):
    """
    Automation for a polygon custom ramp.

    Takes a polygon custom ramp specification as a dictionary and stores a list of sld.GsSldPolygonSymbolizer:

    polygonCustomRamp = {
        "class": sld.SemiologyPolygonCustomRamp,
        "stroke": stroke,
        "colors": ["#ff0000", "#00ff00", "#0000ff"]
    }
    """

    def __init__(self, params):
        self.out = []

        for i in params["colors"]:
            o = core.GsSldPolygonSymbolizer()

            if "stroke" in params.keys():
                o.addSymbol(SemiologyStroke(params["stroke"])())
                
            o.addSymbol(SemiologyFill({"color": i})())

            self.out.append(o)



class FilterGtoe(Automation):
    """
    Automation for GTOE filter.

    Takes a filter specification as a dictionary and stores a 
    


class StyleCustom(Automation):
    """
    Automation for a full custom SLD style.

    Takes a style specification as a dictionary and builds a full SLD. See test_18_automation.py for examples.
    """

    def __init__(self, params):
        symbols = [str(a["class"](a)()) for a in params["symbols"]]
        rules = [a["class"](a)() if isinstance(a, dict) else a for a in params["rules"]]
        filters = [a["class"](a)() if isinstance(a, dict) else a for a in params["filters"]]

        print
        print symbols
        print
        print rules
        print
        print filters

        ft = core.GsFeatureTyleStyle()
        
        for i in range(0, len(rules)):
            pass
            
