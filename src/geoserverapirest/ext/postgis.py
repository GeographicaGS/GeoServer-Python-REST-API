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
    u"int4": "java.lang.Integer",
    u"varchar": "java.lang.String",
    u"geometry.ST_MultiPolygon": "com.vividsolutions.jts.geom.MultiPolygon",
    u"float8": "java.lang.Double"
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
        
    
    def getFieldsFromTable(self, schema, table, geomColumn):
        """
        Returns a dictionary with the fields structured expected
        by core.GsInstance.createFeatureTypeFromPostGisTable. It's just a
        convenience wrapper around the more general getFieldsFromSql.

        :param schema: Table's schema.
        :type schema: String
        :param table: Table name.
        :type table: String
        :param geomColumn: The name of the geometry column to be used in the table.
        :type geomColumn: String
        :return: A dictionary to insert into a create feature request.
        :rtype: Dict
        """

        sql = "select * from %s.%s;" % (schema, table)

        return self.getFieldsFromSql(sql, geomColumn)


    def getFieldsFromSql(self, sql, geomColumn):
        """
        Returns a Dict with columns structure as expected by
        core.GsInstance.createFeatureTypeFromPostGisTable from a psycopg2
        cursor's column description spawning from a SQL and a
        geometry column name returned by the given SQL. Each column data type
        is mapped to the correct Java data type. Only supports by now a single
        geometry column.

        :param sql: SQL to analyze.
        :type sql: String
        :param geomColumn: Geometry column within SQL to analyze.
        :type geomColumn: String
        :return: A dictionary to insert into a create feature request.
        :rtype: Dict
        """

        dataTypes = self._getPgDataTypes()

        # Get columns
        cur = self._conn.cursor()
        cur.execute(sql)
        columns = cur.description
        cur.close()

        import pytest
        pytest.set_trace()
        
        # Analyze geometry column (check SRID and geometry type)
        try:
            sql = """
            select distinct
              st_srid(%s),
              st_geometrytype(%s)
            from
              (%s) a;
            """ % (geomColumn, geomColumn, sql)

            cur = self._conn.cursor()
            cur.execute(sql)
            res = cur.fetchall()
            cur.close()
        except:
            raise PostGisException("Something happen while checking geom column %s traits." % \
                                    geomColumn)
        
        if len(res)>1:
            raise PostGisException("Not homogeneous SRID or geometry type: %s." % res)
        elif len(res)==0:
            raise PostGisException("geom column %s seems to be empty." % geomColumn)
        else:
            geometryTraits = res[0]
        
        out = {u"attributes": {u"attribute": []}}

        for i in columns:
            field = {}
            field[u"maxOccurs"] = 1
            field[u"minOccurs"] = 0
            field[u"nillable"] = True
            field[u"name"] = i[0]
            dataType = dataTypes[i[1]]
            
            if dataType=="geometry":
                field[u"binding"] = typeConversion["geometry."+geometryTraits[1]]
            else:
                field[u"binding"] = typeConversion[dataType]

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

            
    def _getPgDataTypes(self):
        """
        Returns a dictionary with the whole catalog of datatypes of the current database.
        Key is the OID of each data type, so it can be matched against psycopg2
        cursor description of columns.

        :return: A dictionary with the data types' OID as keys and the name of the data type as value.
        :rtype: Dict
        """

        types = {}
        cur = self._conn.cursor()
        sql = "select oid, * from pg_type;"
        cur.execute(sql)

        for r in cur:
            types[r[0]]=r[1]
            
        cur.close()

        return types
        

    
class PostGisException(Exception):
    """
    Exception class for PostGIS adapter.
    """

    def __init__(self, explanation):
        self.explanation = explanation


    def __str__(self):
        return "Exception in PostGIS adapter: %s" % self.explanation
    
