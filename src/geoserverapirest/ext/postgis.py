#!/usr/bin/env python
# coding=UTF-8

"""
This submodule handles PostGIS operations.
"""

import psycopg2 as pg
from psycopg2.extensions import AsIs


"""
TODO: The first of this conversions are here for function getFieldsFromTable. When merged to work like
getFieldsFromSql, remove them.
"""

typeConversion = {
    u"int4": u"java.lang.Integer",
    u"varchar": u"java.lang.String",
    u"geometry.MULTIPOLYGON": "com.vividsolutions.jts.geom.MultiPolygon",



    # TODO: To deprecate
    u"_int4": u"java.lang.Integer",
    u"_varchar": u"java.lang.String",
    u"_geometry": u"com.vividsolutions.jts.geom."
}



class GsPostGis(object):
    """
    This class is a bunch of helpers for working with the PostGIS.
    """

    _conn = None
    """
    psycopg2 connection object.
    """

    _dataTypes = None
    """
    Data type codes for casting.
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

        # Get data types
        cur = self._conn.cursor()
        q = """select typname,typelem from pg_catalog.pg_type;"""
        cur.execute(q)
        types = cur.fetchall()
        self._dataTypes = {i[1]: i[0] for i in types}
        cur.close()
        

    def close(self):
        """
        Closes the connection.
        """

        self._conn.close()
        
    
    def getFieldsFromTable(self, schema, table):
        """
        Returns a dictionary with the fields structured expected
        by core.GsInstance.createFeatureTypeFromPostGisTable.

        :param schema: Table's schema.
        :type schema: String
        :param table: Table name.
        :type table: String

        .. todo:: try to get the field information from psycopg2 and not from PG information schema. Make this function compatible with the following one.
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


    def getFieldsFromSql(self, sql, geomColumn, geomType):
        """
        Returns a dictionary with the fields structured expected
        by core.GsInstance.createFeatureTypeFromPostGisTable.

        :param sql: SQL to analyze.
        :type sql: String
        :param geomColumn: Name of the column containing the geometry.
        :type geomColumn: String
        :param geomType: Type of the geometry. Can be Polygon, MultiPolygon, ...
        :type geomType: String
        :return: Dict structure with field schema.
        :rtype: Dict

        .. todo:: Geometry type and srid are guessable from studying the column with type "_geometry"
        .. todo:: Perhaps the process of getting the dictionary structure should be left to the Feature Type creation functions in core. Just leave here the _analyzeFields, including information about the EPSG, for example.
        """

        cur = self._conn.cursor()
        cur.execute(sql)
        fields = self._analyzeFields(cur.description)
        cur.close()
        out = {u"attributes": {u"attribute": []}}

        for i in fields:
            field = {}
            field[u"maxOccurs"] = 1
            field[u"minOccurs"] = 0
            field[u"nillable"] = True
            field[u"name"] = i["name"]

            if i["type"]=="_geometry":
                field[u"binding"] = typeConversion[i["type"]]+geomType
            else:
                field[u"binding"] = typeConversion[i["type"]]

            out["attributes"]["attribute"].append(field)
                        
        return out


    def getColumnMinMax(self, table, column):
        """
        Returns the min / max values found in a column in a table.

        :param table: Fully qualified table name.
        :type table: String
        :param column: Column name.
        :type column: String
        """

        cur = self._conn.cursor()
        
        sql = "select min(%s) from %s"
        cur.execute(sql, (AsIs(column), AsIs(table)))
        min = cur.next()
        
        sql = "select max(%s) from %s"
        cur.execute(sql, (AsIs(column), AsIs(table)))
        max = cur.next()
        
        # import pytest
        # pytest.set_trace()


        #####HERE######    

    def _analyzeFields(self, cursorDescription):
        """
        Returns a dictionary with column descriptions from cursor description.

        :param cursorDescription: The cursor description to analyze.

        .. todo:: this function should be the only one here. The getFieldsXXX functionality should move to the respective create functions at core. Guess geometry properties and add new dictionary data items to store them (geometry type and epsg).
        """
        
        out = []

        for i in cursorDescription:
            field = {}
            field["type"] = self._dataTypes[i[1]]
            field["name"] = i[0]
            field["length"] = i[3]
            out.append(field)

        return out
