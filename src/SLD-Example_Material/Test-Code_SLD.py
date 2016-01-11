#!/usr/bin/env python
# coding=UTF-8

import geoserverapirest.ext.sld as sld
import xml.etree.ElementTree as x
reload(sld)

# Creates polygon symbol
fill = sld.GsSldFillSymbolizer("#000000")
stroke = sld.GsSldStrokeSymbolizer("#000000", 0.25, "bevel")
polySym = sld.GsSldPolygonSymbolizer()
polySym.addSymbol(fill)
polySym.addSymbol(stroke)

# Creates rule condition
c1 = sld.GsSldCondition("GT", "area", 3)
c2 = sld.GsSldCondition("LTOE", "area", 4)
c1.composite(c2, "And")
filter = sld.GsSldFilter()
filter.addCondition(c1)

# Create rule
rule = sld.GsSldRule("A rule", "This is a rule")
rule.addSymbolizer(polySym)
rule.addFilter(filter)

# Put everything together
featureTypeStyle = sld.GsSldFeatureTypeStyle()
featureTypeStyle.addRule(rule)
userStyle = sld.GsSldUserStyle("municipio")
userStyle.addFeatureTypeStyle(featureTypeStyle)
namedLayer = sld.GsSldNamedLayer("municipio")
namedLayer.addUserStyle(userStyle)

root = sld.GsSldRoot()
root.addNamedLayer(namedLayer)

print str(root)

