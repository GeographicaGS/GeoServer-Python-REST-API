#!/usr/bin/env python
# coding=UTF-8

"""
This submodule handles PostGIS operations.
"""

import psycopg2 as pg

typeConversion = {
    u"int4": u"java.lang.Integer",
    u"varchar": u"java.lang.String",
    u"geometry.MULTIPOLYGON": "com.vividsolutions.jts.geom.MultiPolygon"
}



class GsPostGis(object):
    """
    This class is a bunch of helpers for working with the PostGIS.
    """

    _conn = None
    """
    psycopg2 connection object.
    """

    
    def __init__(self, host, port, database, user, password):
        """
        Creates a connection to the PostGIS.

        :param host: PostGIS host.
        :type host: String
        :param port: PostGIS port.
        :type port: String
        :param database: PostGIS database.
        :type database: String
        :param user: PostGIS user.
        :type user: String
        :param password: PostGIS password.
        :type password: String
        """
        
        self._conn = pg.connect(database=database, user=user, \
                                password=password, port=port, \
                                host=host)


    def close(self):
        """
        Closes the connection.
        """

        self._conn.close()
        
    
    def getFields(self, schema, table):
        """
        Returns a dictionary with the fields structured expected
        by core.GsInstance.createFeatureTypeFromPostGisTable.

        :param schema: Table's schema.
        :type schema: String
        :param table: Table name.
        :type table: String
        """

        cur = self._conn.cursor()

        q = """
        select
          a.column_name,
          a.udt_name,
          a.character_maximum_length,
          b.coord_dimension,
          b.srid,
          b.type
        from
          information_schema.columns a left join
          public.geometry_columns b on
          a.table_catalog=b.f_table_catalog and
          a.table_schema=b.f_table_schema and
          a.table_name=b.f_table_name and
          a.column_name=b.f_geometry_column
        where
          table_schema=%s and table_name=%s
        order by
          ordinal_position;
        """
        
        cur.execute(q, (schema, table))
        fields = cur.fetchall()
        cur.close()

        out = {u"attributes": {u"attribute": []}}

        for i in fields:
            field = {}
            field[u"maxOccurs"] = 1
            field[u"minOccurs"] = 0
            field[u"nillable"] = True
            field[u"name"] = i[0]

            if i[1]=="geometry":
                field[u"binding"] = typeConversion["geometry."+i[5]]
            else:
                field[u"binding"] = typeConversion[i[1]]

            out["attributes"]["attribute"].append(field)
            
        return out
