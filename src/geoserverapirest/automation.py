#!/usr/bin/env python
# coding=UTF-8

import geoserverapirest.core as core

# --------------------------------------
# Automation for dictionaries of objects
# --------------------------------------

class AutomateDict(object):
    """
    This class automates creation of dictionaries of objects in a GeoServer instance.
    """

    gsInstance = None
    
    def __init__(self, geoserverInstance):
        """
        Automates creation of dictionaries of objects in a GeoServer instance.

        :param geoserverInstance: Dictionary of GeoServer instance connection data.
        :type geoserverInstance: Dict
        """

        self.gsInstance = core.GsInstance(geoserverInstance["url"], geoserverInstance["user"], \
                                          geoserverInstance["pass"])

    def automateStyles(self, styles):
        """
        Automates style creation from a dict of styles.

        :param styles: Dict with styles.
        :type styles: Dict
        """
        
        if self.gsInstance.checkAlive()==200:
            print "Target GeoServer active..."

            existingStyles = self.gsInstance.getStyleNames()
            
            for name, style in styles.iteritems():
                if name not in existingStyles:
                    print "Creating style %s: " % name
                    rest = self.gsInstance.createStyle(name, str(style["class"](style)()))
                    print rest==200
                else:
                    print "Style %s already exists" % name
        else:
            print "Target GeoServer unreachable!"

            

    def automateLayers(self, layers):
        """
        Automate layer creation. See tests for an example.
    
        :param layers: A layers description dictionary.
        :type layers: Dict
        """
    
        existingLayers = self.gsInstance.getLayerNames()
    
        if self.gsInstance.checkAlive()==200:
            print "Target GeoServer active..."
            
            # Creating layers
            for name, layer in layers.iteritems():
                if name not in existingLayers: 
                    print "Creating layer %s: " % name
                    
                    # Generate Feature Type
                    if layer["type"]=="sql":
                        r = self.gsInstance.createFeatureTypeFromPostGisQuery( \
                                layer["workspace"], layer["datastore"], \
                                layer["sql"], layer["idcolumn"], \
                                layer["geomcolumn"], name, \
                                layer["title"], layer["postgis"]["pass"])
                                
                    elif layer["type"]=="table":
                        r = self.gsInstance.createFeatureTypeFromPostGisTable( \
                                layer["workspace"], layer["datastore"], \
                                layer["table"], layer["geomcolumn"], \
                                name, layer["title"], layer["postgis"]["pass"])
    
                    else:
                        print "Unrecognized layer type."
                                
                    print r==201
                                                              
                    r = self.gsInstance.updateLayer(name, styles=layer["styles"], \
                                        defaultStyle=layer["styles"][0])
            
                    print "Updating layer %s: " % name
                    print r==200
                else:
                    print "Layer %s already exists." % name
        
        else:
            print "Target GeoServer unreachable!"
            
