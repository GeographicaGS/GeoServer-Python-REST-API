#!/usr/bin/env python
# coding=UTF-8

import geoserverapirest.ext.sld.core as core, geoserverapirest.ext.sld.color as color
import geoserverapirest.ext.sld.ranges as ranges

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




# -----------------
# Semiology Classes
# -----------------    
    
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
        "low": "#dedece",
        "high": "#4a4140"
    }
    """

    def __init__(self, params, steps):
        self.out = []

        c = color.Color()
        colors = c.colorRamp(params["low"], params["high"], steps)

        for i in range(0, steps):
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

    def __init__(self, params, sidesteps):
        self.out = []

        c = color.Color()
        colors = c.colorDualRamp(params["low"], params["middle"], params["high"], sidesteps)

        for i in range(0, (sidesteps*2)+1):
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



# -----------------
# Condition Classes
# -----------------    

class ConditionGtoe(Automation):
    """
    Automation for GTOE condition.

    Takes a condition specification as a dictionary and stores a GsSldConditionGtoe:

    ConditionGtoe = {
        "class": sld.ConditionGtoe,
        "attribute": "area",
        "value": 20000000
    }
    """

    def __init__(self, params):
        self.out = core.GsSldConditionGtoe(params["attribute"], params["value"])


class ConditionLtoe(Automation):
    """
    Automation for LTOE condition.

    Takes a condition specification as a dictionary and stores a GsSldConditionLtoe:

    ConditionLtoe = {
        "class": sld.ConditionLtoe,
        "attribute": "area",
        "value": 20000000
    }
    """

    def __init__(self, params):
        self.out = core.GsSldConditionLtoe(params["attribute"], params["value"])


class ConditionEqual(Automation):
    """
    Automation for EQUAL condition.

    Takes a condition specification as a dictionary and stores a GsSldConditionEqual:

    ConditionEqual = {
        "class": sld.ConditionEqual,
        "attribute": "PROVINCIA",
        "value": "Córdoba"
    }
    """

    def __init__(self, params):
        self.out = core.GsSldConditionEqual(params["attribute"], params["value"])


class ConditionAnd(Automation):
    """
    Automation for AND condition.

    Takes a condition specification as a dictionary and stores a GsSldConditionAnd:

    conditionAnd = {
        "class": sld.ConditionAnd,
        "c0": conditionLtoe,
        "c1": conditionEqual
    }
    """

    def __init__(self, params):
        self.out = core.GsSldConditionAnd(params["c0"]["class"](params["c0"])(), params["c1"]["class"](params["c1"])())


class ConditionOr(Automation):
    """
    Automation for OR condition.

    Takes a condition specification as a dictionary and stores a GsSldConditionOr:

    conditionOr = {
        "class": sld.ConditionOr,
        "c0": conditionLtoe,
        "c1": conditionEqual
    }
    """

    def __init__(self, params):
        self.out = core.GsSldConditionOr(params["c0"]["class"](params["c0"])(), params["c1"]["class"](params["c1"])()
)



# -----------------
# Ranges automation
# -----------------

class RangesQuartile(Automation):
    """
    Automation for a quartile range calculation.

    :param data: Data to create intervals from.
    :type data: List
    :param intervals: Number of intervals
    :type intervals: integer
    :param precision: Precision
    :type precision: integer
    """

    def __init__(self, data, intervals, precision):
        a = ranges.Range()

        self.out = a.quartileInterval(data, intervals, precision)


class RangesEqual(Automation):
    """
    Automation for a equal range calculation.

    :param data: Data to create intervals from.
    :type data: List
    :param intervals: Number of intervals
    :type intervals: integer
    :param precision: Precision
    :type precision: integer
    """

    def __init__(self, data, intervals, precision):
        a = ranges.Range()

        self.out = a.equalInterval(data, intervals, precision)

                                
class RangesJenksMiddle(Automation):
    """
    Automation for a Jenks middle range calculation.

    :param data: Data to create intervals from.
    :type data: List
    :param sideIntervals: Number of side intervals
    :type sideIntervals: integer
    :param precision: Precision
    :type precision: integer
    """

    def __init__(self, data, sideIntervals, middleValue, precision):
        a = ranges.Range()

        self.out = a.jenksMiddleInterval(data, sideIntervals, middleValue, precision)


class RangesJenks(Automation):
    """
    Automation for a jenks range calculation.

    :param data: Data to create intervals from.
    :type data: List
    :param intervals: Number of intervals
    :type intervals: integer
    :param precision: Precision
    :type precision: integer
    """

    def __init__(self, data, intervals, precision):
        a = ranges.Range()

        self.out = a.jenksInterval(data, intervals, precision)
                    

# ---------------------
# Full style automation
# ---------------------

class StyleBuilder(object):
    """
    This is the base style builder.

    :param namedLayerName: Name of the named layer
    :type namedLayerName: String
    :param styleName: Name of the style
    :type styleName: String
    :param ruleNames: A list of Strings with the names of the rules.
    :type ruleNames: List
    :param conditions: A list of geoserverapirest.ext.sld.core.GsSldConditionXXX with the conditions.
    :type conditions: List
    :param symbols: A list of geoserverapirest.ext.sld.core.GsSldPolygonSymbolizer with the symbolizers.
    :type symbols: List
    """

    @staticmethod
    def build(namedLayerName, styleName, ruleNames, conditions, symbols):
        ft = core.GsSldFeatureTypeStyle()
        
        filters = []

        if conditions is not None:
            for i in conditions:
                if i is not None:
                    filter = core.GsSldFilter()
                    filter.addCondition(i)
                    
                    filters.append(filter)
                else:
                    filters.append(i)
                
        for i in range(0, len(ruleNames)):
            r = core.GsSldRule(ruleNames[i].replace(" ", "_").lower(), ruleNames[i])
            r.addSymbolizer(symbols[i])

            if filters<>[]:
                if filters[i] is not None:
                    r.addFilter(filters[i])

            ft.addRule(r)

        us = core.GsSldUserStyle(styleName)
        us.addFeatureTypeStyle(ft)

        nl = core.GsSldNamedLayer(namedLayerName)
        nl.addUserStyle(us)

        root = core.GsSldRoot()
        root.addNamedLayer(nl)

        return root
    

class StyleCustom(Automation):
    """
    Automation for a full custom SLD style.

    Takes a style specification as a dictionary and builds a full SLD. See test_18_automation.py for examples.
    """

    def __init__(self, params):
        symbols = [a["class"](a)() for a in params["symbols"]]
        conditions = [a["class"](a)() for a in params["conditions"]] if "conditions" in params.keys() else None

        self.out = StyleBuilder.build(params["namedlayername"], params["stylename"], params["rulenames"], conditions, symbols)


class StyleSimpleIntervals(Automation):
    """
    Automation for a simple intervals SLD style.

    Takes a style specification as a dictionary and builds a full SLD. See test_18_automation.py for examples.
    """

    def __init__(self, params):
        data = params["datasource"]["class"](params["datasource"])()
        rang = params["rangetype"](data, params["steps"], params["precision"])()

        conditions = []

        for r in rang:
            c = {"class": ConditionAnd,
                 "c0": {
                    "class": ConditionGtoe,
                    "attribute": params["datasource"]["attributename"],
                    "value": r[0]},
                 "c1": {
                    "class": ConditionLtoe,
                    "attribute": params["datasource"]["attributename"],
                    "value": r[1]}}

            conditions.append(c["class"](c)())

        symbols = params["ramp"]["class"](params["ramp"], params["steps"])()

        rn = ranges.RuleNames()
        
        ruleNames = rn.ruleNames(rang, params["rulenames"]["mono"], params["rulenames"]["dual"], params["rulenames"]["lambda"])

        self.out = StyleBuilder.build(params["namedlayername"], params["stylename"], ruleNames, conditions, symbols)


class StyleCenteredIntervals(Automation):
    """
    Automation for a double ramp.

    Takes a style specification as a dictionary and builds a full SLD. See test_18_automation.py for examples.
    """

    def __init__(self, params):
        data = params["datasource"]["class"](params["datasource"])()

        # Data below and above median
        below = [a for a in data if a<params["mediandata"]]
        above = [a for a in data if a>params["mediandata"]]

        #TODO: Erase median Jenks. A waste of time

        belowIntervals = params["rangetype"](below, params["steps"], params["precision"])()
        aboveIntervals = params["rangetype"](above, params["steps"], params["precision"])()
        
        belowIntervals.append([params["mediandata"], params["mediandata"]])
        belowIntervals.extend(aboveIntervals)

        conditions = []

        # TODO: This is duplicated in the class above, take apart
        for r in belowIntervals:
            c = {"class": ConditionAnd,
                 "c0": {
                    "class": ConditionGtoe,
                    "attribute": params["datasource"]["attributename"],
                    "value": r[0]},
                 "c1": {
                    "class": ConditionLtoe,
                    "attribute": params["datasource"]["attributename"],
                    "value": r[1]}}

            conditions.append(c["class"](c)())
            
        symbols = params["ramp"]["class"](params["ramp"], params["steps"])()

        rn = ranges.RuleNames()
        
        ruleNames = rn.ruleNames(belowIntervals, params["rulenames"]["mono"], params["rulenames"]["dual"], \
                                 params["rulenames"]["lambda"])

        self.out = StyleBuilder.build(params["namedlayername"], params["stylename"], ruleNames, conditions, symbols)
