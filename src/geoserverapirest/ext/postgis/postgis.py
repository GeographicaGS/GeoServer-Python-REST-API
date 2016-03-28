#!/usr/bin/env python
# coding=UTF-8

import core

"""
This module contains helper classes for serializing services to a GeoServer.
"""


class PostGisDataSource(object):
    """
    A PostGIS data origin. This is a helper class for serializing layers to a GeoServer.
    """

    out = None
    
    def __init__(self, params):
        pg = core.GsPostGis(params["postgis"])
        
        # An SQL or a table?
        if "sql" in params["source"].keys():
            self.out = pg.getColumnDataFromSql(params["source"]["sql"])
        else:
            self.out = pg.getColumnDataFromTable(params["source"]["schema"], params["source"]["table"], params["source"]["column"],
                                                 sort=params["source"]["sort"], reverse=params["source"]["reverse"],
                                                 distinct=params["source"]["distinct"])
                    
        pg.close()


    def __call__(self):
        """
        Treat self.out as itself.
        """
        return self.out
    
