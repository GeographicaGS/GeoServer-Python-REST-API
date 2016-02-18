#!/usr/bin/env python
# coding=UTF-8

"""
Helper functions to automate styles and layers creation.
"""

import geoserverapirest.core as gs
reload(gs)
import geoserverapirest.ext.postgis as pg
reload(pg)
import geoserverapirest.ext.sld as sld
reload(sld)
# import config_layers as layers
# import config as c


def automateStyles(geoserver, postgis, styles):
    """
    Automates style creation. See tests for an example.

    :param geoserver: A GeoServer description dictionary.
    :type geoserver: Dict
    :param postgis: A PostGIS description dictionary.
    :type postgis: Dict
    :param styles: A styles description dictionary.
    :type styles: Dict
    """

    gsi = gs.GsInstance(geoserver["url"], geoserver["user"], geoserver["pass"])
    pgi = pg.GsPostGis(postgis["host"], postgis["port"], postgis["db"], postgis["user"], postgis["pass"])

    if gsi.checkAlive()==200:
        print "Target GeoServer active..."

        color = sld.Color()
        rangeBuilder = sld.Range()
        styleBuilder = sld.GsSldStyles()
        existingStyles = gsi.getStyleNames()

        # Creating styles    
        for name, style in styles.iteritems():
            if name not in existingStyles:
                print "Creating style %s: " % name
                
                data = pgi.getColumnData(style["schema"], style["table"], style["column"], \
                                         sort=True)
        
                if style["segmentationType"] in ["quartile", "equal", "jenks"]:
                    fills = color.colorRamp(style["colorScheme"]["low"], \
                                            style["colorScheme"]["high"], \
                                            style["intervals"])
        
                if style["segmentationType"]=="quartile":
                    ranges = rangeBuilder.quartileInterval(data, style["intervals"], style["precision"])
                elif style["segmentationType"]=="equal":
                    ranges = rangeBuilder.equalInterval(data, style["intervals"], style["precision"])
                elif style["segmentationType"]=="jenks":
                    ranges = rangeBuilder.jenksInterval(data, style["intervals"], style["precision"])
        
                featureTypeStyle = sld.GsSldFeatureTypeStyle()
        
                ruleTitles = styleBuilder.buildRuleTitles(ranges, style["dualRuleTitles"], \
                                                          style["monoRuleTitles"], ruleTitleLambdas = \
                                                          style["ruleTitleLambda"])
                
                styleBuilder.createFeatureTypeStyle(featureTypeStyle, fills, None, None, \
                                                    style["column"], ranges, ruleTitles)
                             
                r = styleBuilder.sldFromFeatureTypeStyle(featureTypeStyle)
        
                rest = gsi.createStyle(name, str(r))
        
                print rest==200
            else:
                print "Style %s already exists." % name
                
        pgi.close()

    else:
        print "Target GeoServer unreachable!"
