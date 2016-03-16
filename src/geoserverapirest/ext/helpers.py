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


# Constants

strokeLineJoin = sld.strokeLineJoin



class Automation(object):
    """
    Automation objects base class.
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
    """

    def __init__(self, params):
        self.out = sld.GsSldStrokeSymbolizer(params["color"], params["width"], params["linejoin"])



class SemiologyFill(Automation):
    """
    Automation for fill semiology.
    """

    def __init__(self, params):
        self.out = sld.GsSldFillSymbolizer(params["color"])

    

class SemiologyPolygonManual(Automation):
    """
    Automation for manual polygon style.
    """

    def __init__(self, params):
        self.out = sld.GsSldPolygonSymbolizer()
        self.out.addSymbol(SemiologyStroke(params["stroke"])())
        self.out.addSymbol(SemiologyFill(params["fill"])())



class SemiologyPolygonDoubleRamp(Automation):
    """
    Automation for polygon double ramp.
    """

    def __init__(self, params):
        pass



class SemiologyPolygonSimpleRamp(Automation):
    """
    Automation for polygon simple ramp.
    """

    def __init__(self, params):
        pass



class SemiologyPolygonManualRamp(Automation):
    """
    Automation for polygon manual ramp.
    """

    def __init__(self, params):
        pass
    
    

class SegmentationQuartile(Automation):
    """
    Automation for quartile segmentation.
    """
    
    def __init__(self, params, data):
        r = sld.Range()

        self.out = r.quartileInterval(data, params["intervals"], params["precision"])



class DataPostGisTable(Automation):
    """
    Automation for extracting data from a PostGIS table.
    """
    
    def __init__(self, params):
        pgi = pg.GsPostGis(params["postgis"])

        self.out = pgi.getColumnDataFromTable(params["schema"], params["table"], params["column"], sort=params["sort"], \
                                              reverse=params["reverse"], distinct=params["distinct"])
        
        pgi.close()


class SemiologySimpleRamp(Automation):
    def __init__(self, params):
        print "SimpleRamp"
        print params
        pass
        

class StyleContinuousIntervals(Automation):
    def __init__(self, params):
        # Segmentation
        # segments = params["segmentation"]["type"](params["segmentation"])
        
        print "Cont"
        print params
        pass


class StyleManualIntervals(Automation):
    def __init__(self, params):
        print "Manual"
        print params
        pass


    

    
            

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

        for name, style in styles.iteritems():
            print name

            e = style["type"](style)

# def automateStyles(geoserver, styles):
#     """
#     Automates style creation. See tests for an example.

#     :param geoserver: A GeoServer description dictionary.
#     :type geoserver: Dict
#     :param styles: A styles description dictionary.
#     :type styles: Dict
#     """

#     gsi = gs.GsInstance(geoserver["url"], geoserver["user"], geoserver["pass"])

#     if gsi.checkAlive()==200:
#         print "Target GeoServer active..."

#         # color = sld.Color()
#         # rangeBuilder = sld.Range()
#         # styleBuilder = sld.GsSldStyles()
#         existingStyles = gsi.getStyleNames()

#         # Creating styles    
#         for name, style in styles.iteritems():

#             # Check if style exists
#             if name not in existingStyles:
#                 print "Creating style %s: " % name

#                 # Continuous intervals style
#                 if style["styleType"]==styleTypes["ContinuousIntervals"]:
#                     pgi = pg.GsPostGis(style["data"]["postgis"])

#                     # Get data
#                     # data = pgi.getColumnData(style
                    
#                     # Check class type
#                     # if style["classes"]["type"]==segmentationTypes["Quartile"]:
                        
                        


#                     pgi.close()

#             else:
#                 print "Style %s already exists." % name

                
                
#         #         data = pgi.getColumnData(style["schema"], style["table"], style["column"], \
#         #                                  sort=True)

                                         
#         #         if style["colorScheme"]["type"]=="colorRamp":
#         #             fills = color.colorRamp(style["colorScheme"]["low"], \
#         #                                     style["colorScheme"]["high"], \
#         #                                     style["intervals"])
                                            
#         #         elif style["colorScheme"]["type"]=="dualRamp":
#         #             fills = color.colorDualRamp(style["colorScheme"]["low"], \
#         #                                         style["colorScheme"]["middle"], \
#         #                                         style["colorScheme"]["high"], \
#         #                                         (style["intervals"]-1)/2)

                                                        
#         #         if style["segmentationType"]=="quartile":
#         #             ranges = rangeBuilder.quartileInterval(data, style["intervals"], \
#         #                                                    style["precision"])
#         #         elif style["segmentationType"]=="equal":
#         #             ranges = rangeBuilder.equalInterval(data, style["intervals"], \
#         #                                                 style["precision"])
#         #         elif style["segmentationType"]=="jenks":
#         #             ranges = rangeBuilder.jenksInterval(data, style["intervals"], \
#         #                                                 style["precision"])
        
#         #         featureTypeStyle = sld.GsSldFeatureTypeStyle()
        
#         #         ruleTitles = \
#         #           styleBuilder.buildRuleTitles(ranges, style["dualRuleTitles"], \
#         #                                        style["monoRuleTitles"], \
#         #                                        ruleTitleLambdas = style["ruleTitleLambda"])
                
#         #         styleBuilder.createFeatureTypeStyle(featureTypeStyle, fills, None, None, \
#         #                                             style["column"], ranges, ruleTitles)
                             
#         #         r = styleBuilder.sldFromFeatureTypeStyle(featureTypeStyle)
        
#         #         rest = gsi.createStyle(name, str(r))
        
#         #         print rest==200
                
#         # pgi.close()

#     else:
#         print "Target GeoServer unreachable!"

                
        
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
