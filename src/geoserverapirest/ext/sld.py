#!/usr/bin/env python
# coding=UTF-8

import math
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
          '<def:StyledLayerDescriptor xmlns:def="http://www.opengis.net/sld" '+ \
          'xmlns:ogc="http://www.opengis.net/ogc" '+ \
          'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '+ \
          'version="1.1.0" xmlns:xlink="http://www.w3.org/1999/xlink" '+ \
          'xsi:schemaLocation="http://www.opengis.net/sld '+ \
          'http://schemas.opengis.net/sld/1.1.0/StyledLayerDescriptor.xsd" '+ \
          'xmlns:se="http://www.opengis.net/se"></def:StyledLayerDescriptor>'
        
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
          '<def:NamedLayer xmlns:se="http://www.opengis.net/se" '+ \
          'xmlns:def="http://www.opengis.net/sld">'+ \
          '<se:Name>%s</se:Name></def:NamedLayer>' % name
                         
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
          '<def:UserStyle xmlns:se="http://www.opengis.net/se" '+ \
          'xmlns:def="http://www.opengis.net/sld">'+ \
          '<se:Name>%s</se:Name></def:UserStyle>' % name

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
        
        xml = '<se:FeatureTypeStyle xmlns:se="http://www.opengis.net/se"></se:FeatureTypeStyle>'

        self.sld = x.fromstring(xml)


    def addRule(self, rule):
        """
        Adds a rule to the FeatureTypeStyle.

        :param rule: The rule to be added.
        :type symbol: xml.etree.ElementTree
        """

        self.sld.insert(1, rule())



class GsSldCondition(GsSldElement):
    """
    Represents an SLD condition for filters.
    """

    def __init__(self, conType, field, value):
        """
        Creates an SLD condition for filters.

        :param conType: Condition type. Available conditions are GT for greater than and LTOE for less than or equal to.
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
            '<se:Rule xmlns:se="http://www.opengis.net/se">'+ \
            '<se:Name>%s</se:Name>' % name+ \
            '<se:Description><se:Title>%s</se:Title></se:Description>' % description+ \
            '</se:Rule>'

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
            '<se:Stroke xmlns:se="http://www.opengis.net/se">'+ \
            '<se:SvgParameter name="stroke">%s</se:SvgParameter>' % color+ \
            '<se:SvgParameter name="stroke-width">%s</se:SvgParameter>' % width+ \
            '<se:SvgParameter name="stroke-linejoin">%s</se:SvgParameter>' % linejoin+ \
            '</se:Stroke>'

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
            '<se:Fill xmlns:se="http://www.opengis.net/se">'+ \
            '<se:SvgParameter name="fill">%s</se:SvgParameter>' % color+ \
            '</se:Fill>'

        self.sld = x.fromstring(xml)

    

class GsSldPolygonSymbolizer(GsSldElement):
    """
    Represents a polygon symbolizer.
    """

    def __init__(self):
        xml = \
            '<se:PolygonSymbolizer xmlns:se="http://www.opengis.net/se">'+ \
            '</se:PolygonSymbolizer>'

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
    
