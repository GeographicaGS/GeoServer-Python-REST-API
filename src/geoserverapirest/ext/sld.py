#!/usr/bin/env python
# coding=UTF-8

import math, colour, random, copy
import xml.etree.ElementTree as x

"""
TODO: All this functions needs proper testing.

TODO: In general, all this functions are very prone to errors in the insertion of elements,
which are to be entered in the right order. Check the example code and the example XML, which are
valid.
"""

class GsSldElement(object):
    """
    This is the base class for SLD elements.
    """

    sld = None
    """SLD element, an xml.etreeElementTree."""


    def __call__(self):
        """
        Treat self.sld() as itself.
        """
        return self.sld


    def __str__(self):
        """
        Return as string.
        """

        return x.tostring(self(), encoding="UTF-8")

    

class GsSldRoot(GsSldElement):
    """
    Represents the element root of a SLD.
    """

    def __init__(self):
        """
        Creates a new SLD root.
        """
        
        xml = \
          '<?xml version="1.0" encoding="UTF-8"?>'+ \
          '<StyledLayerDescriptor version="1.0.0" '+ \
          'xmlns:ogc="http://www.opengis.net/ogc" '+ \
          'xmlns="http://www.opengis.net/sld"></StyledLayerDescriptor>'
        
        self.sld = x.fromstring(xml)


    def addNamedLayer(self, namedLayer):
        """
        Adds a named layer to the SLD root.

        :param namedLayer: The named layer to be added.
        :type namedLayer: xml.etree.ElementTree
        """

        self.sld.insert(1, namedLayer())

        

class GsSldNamedLayer(GsSldElement):
    """
    Represents a NamedLayer.
    """

    def __init__(self, name):
        """
        Creates a new NamedLayer.

        :param name: Name of the new NamedLayer.
        :type name: String
        """

        xml = \
          '<NamedLayer>'+ \
          '<Name>%s</Name></NamedLayer>' % name
                         
        self.sld = x.fromstring(xml)


    def addUserStyle(self, userStyle):
        """
        Adds a user style to the NamedLayer.

        :param userStyle: The user style to be added.
        :type userStyle: xml.etree.ElementTree
        """

        self.sld.insert(1, userStyle())


    
class GsSldUserStyle(GsSldElement):
    """
    Represents a UserStyle.
    """

    def __init__(self, name):
        """
        :param name: Name of the new UserStyle.
        :type name: String
        """

        xml = \
          '<UserStyle>'+ \
          '<Name>%s</Name></UserStyle>' % name

        self.sld = x.fromstring(xml)


    def addFeatureTypeStyle(self, featureTypeStyle):
        """
        Adds a FeatureTypeStyle.

        :param featureTypeStyle: The FeatureTypeStyle to be added.
        :type featureTypeStyle: xml.etree.ElementTree
        """

        self.sld.insert(1, featureTypeStyle())



class GsSldFeatureTypeStyle(GsSldElement):
    """
    Represents a FeatureTypeStyle element.
    """

    def __init__(self):
        """
        Creates a new FeatureTypeStyle element.
        """
        
        xml = '<FeatureTypeStyle></FeatureTypeStyle>'

        self.sld = x.fromstring(xml)


    def addRule(self, rule):
        """
        Adds a rule to the FeatureTypeStyle.

        :param rule: The rule to be added.
        :type symbol: xml.etree.ElementTree
        """

        self.sld.insert(0, rule())



class GsSldCondition(GsSldElement):
    """
    Represents an SLD condition for filters.
    """

    def __init__(self, conType, field, value):
        """
        Creates an SLD condition for filters.

        :param conType: Condition type. Available conditions are GT for greater than, GTOE for greater than or equal to and LTOE for less than or equal to.
        :type: String
        :param field: Field to apply the condition to.
        :type: String
        :param value: Condition value.
        :type value: String
        """

        if conType=='GT':
            cond = "PropertyIsGreaterThan"
        elif conType=='LTOE':
            cond = "PropertyIsLessThanOrEqualTo"
        elif conType=="GTOE":
            cond = "PropertyIsGreaterThanOrEqualTo"
        else:
            raise SldException("Unknown SLD filter condition.")
            
        xml = \
            '<ogc:%s xmlns:ogc="http://www.opengis.net/ogc">' % cond + \
            '<ogc:PropertyName>%s</ogc:PropertyName>' % field + \
            '<ogc:Literal>%s</ogc:Literal>' % value + \
            '</ogc:%s>' % cond

        self.sld = x.fromstring(xml)
        

    def composite(self, rule, boolean):
        """
        Composites the present condition with another one.

        :param rule: Rule to compose this with, or a list of rules to compose with this. >> TODO
        :type rule: xml.etree.ElementTree
        :param boolean: Boolean operator to compose. And and Or are valid values.
        :type boolean: String
        """

        xml = '<ogc:%s xmlns:ogc="http://www.opengis.net/ogc"></ogc:%s>' % (boolean, boolean)
        comp = x.fromstring(xml)
        comp.insert(0, rule.sld)
        comp.insert(0, self.sld)
        self.sld = comp
        
        

class GsSldFilter(GsSldElement):
    """
    Represents an SLD Filter.
    """

    def __init__(self):
        """
        Creates a new SLD filter.
        """

        xml = '<ogc:Filter xmlns:ogc="http://www.opengis.net/ogc"></ogc:Filter>'

        self.sld = x.fromstring(xml)


    def addCondition(self, condition):
        """
        Adds a condition to the filter.

        TODO: Do a lot of isinstance checks in all members.

        :param condition: The condition to be added.
        :type: xml.etree.ElementTree
        """

        self.sld.insert(0, condition())
        


class GsSldRule(GsSldElement):
    """
    Represents an SLD rule.
    """

    def __init__(self, name, description):
        """
        Creates a new SLD rule.

        :param name: Rule name.
        :type name: String
        :param description: Description name.
        :type description: String
        """
        
        xml = \
            '<Rule>'+ \
            '<Name>%s</Name>' % name+ \
            '<Title>%s</Title>' % description+ \
            '</Rule>'

        self.sld = x.fromstring(xml)


    def addSymbolizer(self, symbolizer):
        """
        Adds a symbolizer to the rule.
        """

        self.sld.insert(2, symbolizer())


    def addFilter(self, filter):
        """
        Adds the filter to the rule.
        """

        self.sld.insert(2, filter())



class GsSldStrokeSymbolizer(GsSldElement):
    """
    Represents a stroke symbolizer.
    """

    def __init__(self, color, width, linejoin):
        """
        Gets a new Stroke symbolizer.

        :param color: A color in the form #RRGGBB.
        :type color: String
        :param width: The width of the stroke.
        :type width: Double
        :param linejoin: The line join style. Possible values are bevel.
        :type linejoin: String
        """

        xml = \
            '<Stroke>'+ \
            '<CssParameter name="stroke">%s</CssParameter>' % color+ \
            '<CssParameter name="stroke-width">%s</CssParameter>' % width+ \
            '<CssParameter name="stroke-linejoin">%s</CssParameter>' % linejoin+ \
            '</Stroke>'

        self.sld = x.fromstring(xml)



class GsSldFillSymbolizer(GsSldElement):
    """
    Represents a fill symbolizer.
    """

    def __init__(self, color):
        """
        Gets a new fill symbolizer.

        :param color: A color in the form #RRGGBB.
        :type color: String
        :return: An xml.etree.ElementTree containing the new fill symbolizer.
        :rtype: xml.etree.ElementTree
        """

        xml = \
            '<Fill>'+ \
            '<CssParameter name="fill">%s</CssParameter>' % color+ \
            '</Fill>'

        self.sld = x.fromstring(xml)

    

class GsSldPolygonSymbolizer(GsSldElement):
    """
    Represents a polygon symbolizer.
    """

    def __init__(self):
        xml = \
            '<PolygonSymbolizer>'+ \
            '</PolygonSymbolizer>'

        self.sld = x.fromstring(xml)


    def addSymbol(self, symbol):
        """
        Adds a symbol to the polygon symbolizer.

        :param symbol: The symbol to be added.
        :type symbol: xml.etree.ElementTree
        """

        self.sld.insert(1, symbol())



class SldException(Exception):
    """
    Exception class for SLD.
    """

    def __init__(self, explanation):
        self.explanation = explanation


    def __str__(self):
        return "Exception in SLD parser: %s" % self.explanation
    


class Range(object):
    """
    This class implements several methods to calculate ranges and data series
    segmentations.
    """

    def __init__(self):
        pass


    def quartileInterval(self, data, intervals, precision):
        """
        Returns quartile intervals. A list of lists of two floats is returned, each one a closed interval.

        :param data: Array of data.
        :type data: List
        :param intervals: Number of intervals.
        :type intervals: Integer
        :param precision: Precision of interval limits, in decimal places.
        :type precision: integer
        :return: A list of lists containing the interval limits as closed intervals on both extremes.
        :rtype: List
        """

        # Prepare data
        data = sorted(data)

        # Interval size
        intSize = int(math.floor(len(data)/intervals))

        # Chop data with intSize. Last interval may be greater if not exactly divisible
        inter = [data[i*intSize:(i+1)*intSize] for i in range(0, intervals-1)]
        inter.append(data[(intervals-1)*intSize:])

        # Retouch intervals so no overlapping values occurs between intervals
        i = 1
        while i<len(inter):
            inter[i] = [k for k in inter[i] if k!=inter[i-1][-1]]

            # Sometimes an empty list is returned            
            if inter[i]==[]:
                del inter[i]
            else:
                i+=1
                        
        # Final closed intervals
        out = [[inter[i][0], inter[i][-1]] for i in range(0, len(inter))]
        
        return out
        

    def equalInterval(self, data, intervals, precision):
        """
        Returns equal intervals. A list of lists of two floats is returned, each a closed interval.

        :param data: Array of data. Just pass [min, max] in case min and max are already know, for example by the function getColumnMinMax in PostGIS submodule.
        :type min: List
        :param intervals: Number of intervals.
        :type intervals: Integer
        :param precision: Precision of interval limits, in decimal places.
        :type precision: Integer
        :return: A list of lists containing the interval limits as closed intervals on both extremes.
        :rtype: List

        .. todo: This function was relocated from SLD and needs proper testing.
        """

        minV = float(min(data))
        maxV = float(max(data))
        
        step = round((maxV-minV)*1.00/intervals, precision)
        precisionStep = math.pow(10, -precision)
        out = []
        
        for i in range(0, intervals):
            out.append([round(minV+(i*step), precision),
                        round(minV+((i+1)*step)-precisionStep, precision)])

        # Redefine upper from last interval
        out[-1][1] = maxV

        return out


    def jenksMiddleInterval(self, data, sideIntervals, middleValue, precision, initialPopulation=50, bestOf=50, \
                      generations=2, bestPopulation=5, mutatedChildrens=2, maxMutations=10):
        """
        Returns Jenks intervals partitioned with a middle value. A list of lists of two floats is returned, each a closed interval.

        :param data: The data sequence.
        :type data: List
        :param intervals: Number of intervals to be computed. Must be less than the different values in the dataset minus one and greater than 0
        :type sideIntervals: Integer
        :param precision: Number of decimals to be used.
        :type precision: Integer
        :return: A list of lists containing the interval limits as closed intervals on both extremes. None if more intervals than data where asked.
        :rtype: List

        .. todo:: create exception, for example to use in this method
        .. todo:: review parameters
        """

        bottomData = [i for i in data if i<middleValue]
        topData =  [i for i in data if i>middleValue]

        bottomRanges = self.jenksInterval(bottomData, sideIntervals, precision)
        topRanges = self.jenksInterval(topData, sideIntervals, precision)

        bottomRanges.append([middleValue, middleValue])
        bottomRanges.extend(topRanges)

        return bottomRanges

        
    def jenksInterval(self, data, intervals, precision, initialPopulation=50, bestOf=50, \
                      generations=2, bestPopulation=5, mutatedChildrens=2, maxMutations=10):
        """
        Returns Jenks intervals. A list of lists of two floats is returned, each a closed interval.

        :param data: The data sequence.
        :type data: List
        :param intervals: Number of intervals to be computed. Must be less than the different values in the dataset minus one and greater than 0
        :type intervals: Integer
        :param precision: Number of decimals to be used.
        :type precision: Integer
        :return: A list of lists containing the interval limits as closed intervals on both extremes. None if more intervals than data where asked.
        :rtype: List

        .. todo:: create exception, for example to use in this method
        .. todo:: review parameters
        """
        
        # Prepare data for precision, erase duplicates and sort data
        data = sorted(list(set([round(i, precision) for i in data])))

        # If intervals is greater than the number of different data -1, return None
        if len(data)-1<intervals or intervals<1:
            return None

        # If intervals is 1, return the data set
        if intervals==1:
            return [[data[0],data[-1]]]
        
        # Dummy best candidate
        bestFinal = {"intervals": [], "gvf": 0}
        bestIterations = 0

        # This is the start of a consecutive search for a best solution
        while bestIterations<bestOf:

            # Initial population: a bunch of different random intervalization
            population = []
            for p in range(0, initialPopulation):
                # First slice point within the dataset
                slicePoints = [random.randint(0, random.randint(1,len(data)-intervals))]

                # Based on the first one, the intermediate
                [slicePoints.append(random.randint(slicePoints[i-1]+1, len(data)-intervals+i)) \
                for i in range(1, intervals)]

                # Final random intervals
                # First
                slices = [data[0:slicePoints[0]+1]]

                # Intermediate ones
                [slices.append(data[slicePoints[i]+1:slicePoints[i+1]+1]) \
                for i in range(0, len(slicePoints)-2)]

                # Last one
                slices.append(data[slicePoints[-2]+1:])

                # Append to population
                population.append({"intervals": slices, "gvf": self._gvf(data, slices)})
            
            generation = 0
                    
            # Iterate generations for a local optima
            while generation<generations:
                # Select the fittest among the current population
                best = sorted([i["gvf"] for i in population], reverse=True)[0:bestPopulation]
                population = [i for i in population if i["gvf"] in best]

                # Create a new population for mutated childrens
                newPopulation = []

                # Iterate current population for mutated childrens
                for i in population:
                    # Generate mutated childrens for current solution
                    for m in range(0, mutatedChildrens):
                        # Copy father
                        inter = copy.deepcopy(i["intervals"])

                        # Initiate mutation sequence
                        for n in range(0, maxMutations):
                            index = random.randint(0,len(inter)-1)
                            side = random.randint(0,1)
                            self._switchElement(inter, index, side)

                        # Add new mutated children to the new population
                        candidate = {"intervals": inter, "gvf": self._gvf(data, inter)}
                        newPopulation.append(candidate)

                # Append new population to the latter generation
                population.extend(newPopulation)

                # Iterate next generation
                generation+=1

            # Get the best of last generation
            bestGvf = sorted([i["gvf"] for i in population], reverse=True)[0]
            bestFit = [i for i in population if i["gvf"]==bestGvf][0]

            # Substitute if better
            if bestFit["gvf"]>bestFinal["gvf"]:
                bestFinal = copy.deepcopy(bestFit)
                
            bestIterations+=1
                                
        # Get the best among all iterations and all generations and prepare final
        # response as closed intervals of values
        ranges = []
        for i in bestFinal["intervals"]:
            if len(i)==1:
                ranges.append([i[0],i[0]])
            else:
                ranges.append([i[0],i[-1]])
        
        return ranges

    
    def _switchElement(self, intervals, index, leftRight):
        """
        Switch an element between intervals. Index gives the left / right
        most element to the left / right neighbour.
        leftRight is 0 for left, or 1 for rigth.
        """
        
        if leftRight==0 and index>0 and len(intervals[index])>1:
            intervals[index-1].append(intervals[index][0])
            del intervals[index][0]

        if leftRight==1 and index<len(intervals)-1 and len(intervals[index])>1:
            intervals[index+1].insert(0, intervals[index][-1])
            del intervals[index][-1]
    
            
    def _divideEvenly(self, data, intervals):
        """
        Divides data in equal intervals for an initial approach to Jenks.
        """
        size = len(data)/intervals
        out = [[0, size]]

        if intervals>1:
            for i in range(1, intervals-1):
                a = [out[i-1][1], out[i-1][1]+size]
                out.append(a)
                
            out.append([out[-1][1], len(data)])

            return [data[a[0]:a[1]] for a in out]
        else:
            return [data]

        
    def _gvf(self, data, intervals):
        """
        Calculates the goodness of fit for a group of intervals.
        """

        sdam = self._sdam(data)
        sdcm = 0

        for i in intervals:
            sdcm = sdcm+self._sdam(i)

        return (sdam-sdcm)/sdam
    

    def _sdam(self, data):
        """
        Calculates the sum of squared deviations for array mean of a list.
        """

        m = sum(data)/len(data)
        return sum([math.pow(i-m, 2) for i in data])

    
    
class Color(object):
    """
    Color manipulation methods.
    """

    def __init__(self):
        pass


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
            c0 = GsSldCondition("GTOE", columnData, ranges[i][0])
            c1 = GsSldCondition("LTOE", columnData, ranges[i][1])
            c0.composite(c1, "And")

            # Generate the filter
            filter = GsSldFilter()
            filter.addCondition(c0)

            # Create rule
            title = ruleTitles[i] % (ruleTitleLambdas[i](ranges[i][0]), \
                                     ruleTitleLambdas[i](ranges[i][1])) if \
                                     "%s" in ruleTitles[i] else ruleTitles[i]
            
            rule = GsSldRule("Rule %s" % i, title)
            rule.addSymbolizer(poly)
            rule.addFilter(filter)

            featureTypeStyle.addRule(rule)


