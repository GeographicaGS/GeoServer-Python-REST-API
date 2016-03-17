#!/usr/bin/env python
# coding=UTF-8

# import math, colour, random, copy

"""
Range and segmentation calculations.
"""


    
class GsSldStyles(object):
    """
    This class is a helper class that uses all the SLD plumbing classes
    to output different kinds of predefined styles. Returns only SLD, do not interact
    with a GeoServer instance from here.
    """

    def buildRuleTitles(self, ranges, dualTitle, monoTitle, ruleTitleLambdas=lambda x: x):
        """
        Returns an automatically generated rule titles based on a set of ranges.

        :param ranges: Ranges to contruct rule titles from.
        :type ranges: List
        :param dualTitle: Title to apply to dual values ranges like [2,3]. Must contain a pair of %s.
        :type dualTitle: String
        :param monoTitle: Title to apply to mono value ranges like [4,4]. Must contain a single %s.
        :type monoTitle: String
        :param ruleTitleLambdas: Lambda function to apply to range values in titles.
        :type ruleTitleLambdas: lambda
        :return: A list of rule titles.
        :rtype: List
        """

        out = []
        for i in ranges:
            if i[0]==i[1]:
                out.append(monoTitle % ruleTitleLambdas(i[0]))
            else:
                out.append(dualTitle % (ruleTitleLambdas(i[0]), ruleTitleLambdas(i[1])))

        return out
        
    
    def sldFromFeatureTypeStyle(self, featureTypeStyle):
        """    
        Returns a complete SLD from a featureTypeStyle.
        """
        
        # Create user style
        userStyle = GsSldUserStyle("Style")
        userStyle.addFeatureTypeStyle(featureTypeStyle)

        # Create named layer
        namedLayer = GsSldNamedLayer("NamedLayer")
        namedLayer.addUserStyle(userStyle)

        # Final SLD
        root = GsSldRoot()
        root.addNamedLayer(namedLayer)

        return root
    
                
    def createFeatureTypeStyle(self, featureTypeStyle, fills, strokes, borderWidths, columnData, \
                                ranges, ruleTitles, ruleTitleLambdas=lambda x: x):
        """
        Gets a featureTypeStyle and appends rules based on fills, strokes, etc.

        Fills, strokes, and ranges must have the same length.

        :param featureTypeStyle: The Feature Type Style to attach rules to.
        :type featureTypeStyle: GsSldFeatureTypeStyle
        :param fills: List of fills colors for each interval. Also a string is possible, cloning the value for each interval.
        :type fills: List or string
        :param strokes: List of stroke colors for each interval. Also a string is possible, cloning the value for each interval. None for no stroke.
        :type strokes: List or string
        :param borderWidths: List of border widths. Also a float is possible, cloning the value for each interval. None for no stroke.
        :type borderWidths: List or float
        :param columnData: Name of the column data.
        :type columnData: string
        :param ranges: List of range limits.
        :type ranges: List
        :param ruleTitle: Rule title. Also a string is possible, cloning the value for each interval.
        :type ruleTitle: List or string
        :param ruleTitleLambdas: List of lambda to decorate values for rule title. Also a lambda is possible, cloning the value for each interval.
        :type ruleTitleLambdas: List or Lambda
        """

        # Check polymorphic parameter
        fills = fills if isinstance(fills, list) else [fills for i in range(0, len(ranges))]
        
        strokes = strokes if isinstance(strokes, list) else [strokes for i in range(0, len(ranges))]
        
        ruleTitles = ruleTitles if isinstance(ruleTitles, list) \
          else [ruleTitles for i in range(0, len(ranges))]
          
        ruleTitleLambdas = ruleTitleLambdas if isinstance(ruleTitleLambdas, list) \
          else [ruleTitleLambdas for i in range(0, len(ranges))]
          
        borderWidths = borderWidths if isinstance(borderWidths, list) \
          else [borderWidths for i in range(0, len(ranges))]
                  
        # Generate style
        for i in range(0, len(ranges)):
            # Generate fill
            fill = GsSldFillSymbolizer(fills[i])

            # Generate border
            if strokes[i] is not None:
                stroke = GsSldStrokeSymbolizer(strokes[i], borderWidths[i], "bevel")
            
            # Generate poly symbol
            poly = GsSldPolygonSymbolizer()
            poly.addSymbol(fill)
            if strokes[i] is not None:
                poly.addSymbol(stroke)

            # Generate rule condition
            cond = GsSldConditionAnd(
                GsSldConditionGtoe(columnData, ranges[i][0]),
                GsSldConditionLtoe(columnData, ranges[i][1]))

            # Generate the filter
            filter = GsSldFilter()
            filter.addCondition(cond)

            # Create rule
            title = ruleTitles[i] % (ruleTitleLambdas[i](ranges[i][0]), \
                                     ruleTitleLambdas[i](ranges[i][1])) if \
                                     "%s" in ruleTitles[i] else ruleTitles[i]
            
            rule = GsSldRule("Rule %s" % i, title)
            rule.addSymbolizer(poly)
            rule.addFilter(filter)

            featureTypeStyle.addRule(rule)
