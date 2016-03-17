#!/usr/bin/env python
# coding=UTF-8

import xml.etree.ElementTree as x

"""
This is the plumbing core SLD module. Only this module handles XML construction, and this classes are not
intended to be used directly. Use the "sld" module instead which is user-friendly and that can be used to easily
serialize SLD definitions in dictionaries  with configuration scripts.

A SLD has the following structure, in terms of classes of this module:

  - GsSldRoot: main container of the SLD
    - GsSldNamedLayer: A single container of a layer
      - GsSldUserStyle: A single user style
        - GsSldFeatureTypeStyle: A single container of rules
          - GsSldRule: A combination of a symbolizer and a filter, several of them
            - GsSldFilter: a data filtering condition
            # One of these
            - GsSldPolygonSymbolizer: Symbolizers
              - GsSldStrokeSymbolizer: Optional
              - GsSldFillSymbolizer: Optional
"""


# Constants

strokeLineJoin={
    "bevel": "bevel"
}



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


        
# -------
# Filters
# -------

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

                
        
class GsSldConditionOr(GsSldElement):
    c0 = None
    c1 = None
    
    def __init__(self, c0, c1):
        self.c0 = c0
        self.c1 = c1

        xml = \
          '<ogc:Or xmlns:ogc="http://www.opengis.net/ogc"></ogc:Or>'

        comp = x.fromstring(xml)
        comp.insert(0, c0.sld)
        comp.insert(0, c1.sld)
        self.sld = comp

        
        
class GsSldConditionAnd(GsSldElement):
    c0 = None
    c1 = None
    
    def __init__(self, c0, c1):
        self.c0 = c0
        self.c1 = c1

        xml = \
          '<ogc:And xmlns:ogc="http://www.opengis.net/ogc"></ogc:And>'

        comp = x.fromstring(xml)
        comp.insert(0, c0.sld)
        comp.insert(0, c1.sld)
        self.sld = comp


        
class GsSldConditionGtoe(GsSldElement):
    field = None
    value = None

    def __init__(self, field, value):
        self.field = field
        self.value = value

        xml = \
            '<ogc:PropertyIsGreaterThanOrEqualTo xmlns:ogc="http://www.opengis.net/ogc">'+ \
            '<ogc:PropertyName>%s</ogc:PropertyName>' % self.field + \
            '<ogc:Literal>%s</ogc:Literal>' % self.value + \
            '</ogc:PropertyIsGreaterThanOrEqualTo>'

        self.sld = x.fromstring(xml)

        

class GsSldConditionLtoe(GsSldElement):
    field = None
    value = None

    def __init__(self, field, value):
        self.field = field
        self.value = value

        xml = \
            '<ogc:PropertyIsLessThanOrEqualTo xmlns:ogc="http://www.opengis.net/ogc">'+ \
            '<ogc:PropertyName>%s</ogc:PropertyName>' % self.field + \
            '<ogc:Literal>%s</ogc:Literal>' % self.value + \
            '</ogc:PropertyIsLessThanOrEqualTo>'

        self.sld = x.fromstring(xml)


        
class GsSldConditionEqual(GsSldElement):
    field = None
    value = None

    def __init__(self, field, value):
        self.field = field
        self.value = value

        xml = \
            '<ogc:PropertyIsEqualTo xmlns:ogc="http://www.opengis.net/ogc">'+ \
            '<ogc:PropertyName>%s</ogc:PropertyName>' % self.field + \
            '<ogc:Literal>%s</ogc:Literal>' % self.value + \
            '</ogc:PropertyIsEqualTo>'

        self.sld = x.fromstring(xml)
        


# -----------
# Symbolizers
# -----------

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
        :param linejoin: The line join style. Possible values are stored at constant strokeLineJoin.
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
