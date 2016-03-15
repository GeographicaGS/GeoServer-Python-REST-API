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


def automateStyles(geoserver, styles):
    """
    Automates style creation. See tests for an example.

    :param geoserver: A GeoServer description dictionary.
    :type geoserver: Dict
    :param styles: A styles description dictionary.
    :type styles: Dict
    """

    gsi = gs.GsInstance(geoserver["url"], geoserver["user"], geoserver["pass"])

    if gsi.checkAlive()==200:
        print "Target GeoServer active..."

        color = sld.Color()
        rangeBuilder = sld.Range()
        styleBuilder = sld.GsSldStyles()
        existingStyles = gsi.getStyleNames()

        # Creating styles    
        for name, style in styles.iteritems():
            pgi = pg.GsPostGis(style["postgis"]["host"], style["postgis"]["port"], \
                               style["postgis"]["db"], style["postgis"]["user"], \
                               style["postgis"]["pass"])

            if name not in existingStyles:
                print "Creating style %s: " % name
                
                data = pgi.getColumnData(style["schema"], style["table"], style["column"], \
                                         sort=True)

                                         
                if style["colorScheme"]["type"]=="colorRamp":
                    fills = color.colorRamp(style["colorScheme"]["low"], \
                                            style["colorScheme"]["high"], \
                                            style["intervals"])
                                            
                elif style["colorScheme"]["type"]=="dualRamp":
                    fills = color.colorDualRamp(style["colorScheme"]["low"], \
                                                style["colorScheme"]["middle"], \
                                                style["colorScheme"]["high"], \
                                                (style["intervals"]-1)/2)

                                                        
                if style["segmentationType"]=="quartile":
                    ranges = rangeBuilder.quartileInterval(data, style["intervals"], \
                                                           style["precision"])
                elif style["segmentationType"]=="equal":
                    ranges = rangeBuilder.equalInterval(data, style["intervals"], \
                                                        style["precision"])
                elif style["segmentationType"]=="jenks":
                    ranges = rangeBuilder.jenksInterval(data, style["intervals"], \
                                                        style["precision"])
        
                featureTypeStyle = sld.GsSldFeatureTypeStyle()
        
                ruleTitles = \
                  styleBuilder.buildRuleTitles(ranges, style["dualRuleTitles"], \
                                               style["monoRuleTitles"], \
                                               ruleTitleLambdas = style["ruleTitleLambda"])
                
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


        
def automateLayers(geoserver, layers):
    """
    Automate layer creation. See tests for an example.

    :param geoserver: A GeoServer description dictionary.
    :type geoserver: Dict
    :param layers: A layers description dictionary.
    :type layers: Dict
    """

    gsi = gs.GsInstance(geoserver["url"], geoserver["user"], geoserver["pass"])
    existingLayers = gsi.getLayerNames()


    if gsi.checkAlive()==200:
        print "Target GeoServer active..."
        
        # Creating layers
        for name, layer in layers.iteritems():
            if name not in existingLayers: 
                print "Creating layer %s: " % name
                
                # Generate Feature Type
                if layer["type"]=="sql":
                    r = gsi.createFeatureTypeFromPostGisQuery( \
                            layer["workspace"], layer["datastore"], \
                            layer["sql"], layer["idcolumn"], \
                            layer["geomcolumn"], name, \
                            layer["title"], layer["postgis"]["pass"])
                            
                elif layer["type"]=="table":
                    r = gsi.createFeatureTypeFromPostGisTable( \
                            layer["workspace"], layer["datastore"], \
                            layer["table"], layer["geomcolumn"], \
                            name, layer["title"], layer["postgis"]["pass"])

                else:
                    print "Unrecognized layer type."
                            
                print r==201
                                                          
                r = gsi.updateLayer(name, styles=layer["styles"], \
                                    defaultStyle=layer["styles"][0])
        
                print "Updating layer %s: " % name
                print r==200
            else:
                print "Layer %s already exists." % name
    
    else:
        print "Target GeoServer unreachable!"
