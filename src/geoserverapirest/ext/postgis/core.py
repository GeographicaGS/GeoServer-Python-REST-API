#!/usr/bin/env python
# coding=UTF-8

"""
This submodule handles PostGIS operations.

TODO: create a function to get the min / max of a query and redo the one taking it from a column
accordingly.
"""

import psycopg2 as pg
from psycopg2.extensions import AsIs


"""
TODO: The first of this conversions are here for function getFieldsFromTable. When merged to work like
getFieldsFromSql, remove them.
"""

typeConversion = {
    u"int4": "java.lang.Integer",
    u"int8": "java.lang.Integer",
    u"numeric": "java.lang.Double",
    u"varchar": "java.lang.String",
    u"geometry.ST_MultiPolygon": "com.vividsolutions.jts.geom.MultiPolygon",
    u"geometry.ST_Polygon": "com.vividsolutions.jts.geom.Polygon",
    u"geometry.ST_Point": "com.vividsolutions.jts.geom.Point",
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
    
    def __init__(self, connection):
        """
        Creates a connection to the PostGIS.

        :param connection: A Dict with connection parameters: host, port, db, user, pass
        :type host: Dict
        """
        
        self._conn = pg.connect(database=connection["db"], user=connection["user"], \
                                password=connection["pass"], port=connection["port"], \
                                host=connection["host"])

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

        sql = "select * from %s.%s" % (schema, table)

        return self.getFieldsFromSql(sql, geomColumn)


    def getFieldsFromSql(self, sql, geomColumn):
        """
        Returns a Dict with columns structure as expected by
        core.GsInstance.createFeatureTypeFromPostGisTable from a psycopg2
        cursor's column description spawning from a SQL and a
        geometry column name returned by the given SQL. Each column data type
        is mapped to the correct Java data type. Only supports by now a single
        geometry column.

        This function is rather strict. It will fail if the table contains mixed
        geometry types and/or inexistent or mixed reference systems. It is the user

        :param sql: SQL to analyze.
        :type sql: String
        :param geomColumn: Geometry column within SQL to analyze.
        :type geomColumn: String
        :return: A dictionary to insert into a create feature request.
        :rtype: Dict

        .. todo:: check for not set reference system
        """

        dataTypes = self.getPgDataTypes()

        # Get columns
        cur = self._conn.cursor()
        cur.execute(sql)
        columns = cur.description
        cur.close()
        geomData = self.analyzeGeomColumnFromSql(sql, geomColumn)
        out = {u"attributes": {u"attribute": []}}

        for i in columns:
            field = {}
            field[u"maxOccurs"] = 1
            field[u"minOccurs"] = 0
            field[u"nillable"] = True
            field[u"name"] = i[0]
            dataType = dataTypes[i[1]]
            
            if dataType=="geometry":
                field[u"binding"] = typeConversion["geometry."+geomData["type"]]
            else:
                field[u"binding"] = typeConversion[dataType]

            out["attributes"]["attribute"].append(field)
            
        return out

        
    def getColumnMinMax(self, schema, table, column):
        """
        Returns the min / max values found in a column in a table.

        Create a more general min / max in SQL.

        :param schema: Table schema name.
        :type schema: String
        :param table: Table name.
        :type table: String
        :param column: Column name.
        :type column: String
        :return: A List in the form min / max
        :rtype: List
        """
        
        cur = self._conn.cursor()
        sql = "select min(%s), max(%s) from %s.%s;"
        cur.execute(sql, (AsIs(column), AsIs(column), AsIs(schema), AsIs(table)))
        results = cur.next()

        return [results[0], results[1]]


    def getColumnDataFromSql(self, sql):
        """
        Returns a list with all values present in a given SQL query. The query must return a single
        column.

        /!\ BIG WARNING: This function is vulnerable to SQL injection. Use with unprivileged user with care.
        
        :param sql: SQL query to extract data.
        :type schema: String
        :param sort: If the data should be sorted by the database.
        :type sort: Boolean
        :param reverse: If the data should be reverse sorted by the database.
        :type reverse: Boolean
        :param distinct: If the data should be returned unique by the database.
        :type distinct: Boolean
        :return: A List with all values.
        :rtype: List
        """

        cur = self._conn.cursor()

        # Execute
        cur.execute(sql)

        # Return an array with values
        return [i[0] for i in cur.fetchall()]
                          

    def getColumnDataFromTable(self, schema, table, column, sort=False, reverse=False, distinct=False):
        """
        Returns a list with all values present in the given column. This is just a wrapper to the more
        general getColumnDataFromSql.

        /!\ BIG WARNING: This function is vulnerable to SQL injection. Use with unprivileged user with care.
        
        :param schema: Table schema name.
        :type schema: String
        :param table: Table name.
        :type table: String
        :param column: Column name.
        :type column: String
        :param sort: If the data should be sorted by the database.
        :type sort: Boolean
        :param reverse: If the data should be reverse sorted by the database.
        :type reverse: Boolean
        :param distinct: If the data should be returned unique by the database.
        :type distinct: Boolean
        :return: A List with all values.
        :rtype: List
        """

        # Construct SQL query
        distinctSql = "distinct" if distinct else ""
        sortSql = "order by %s" % column if sort else ""
        sortSql = sortSql+" desc" if sort and reverse else sortSql
        sql = "select %s %s from %s.%s where %s is not null %s;" % (distinctSql, column, schema, table, column, sortSql)

        # Return an array with values
        return self.getColumnDataFromSql(sql)
                          
        
    def analyzeGeomColumnFromTable(self, schema, table, geomColumn):
        """
        Analyzes a geometry column for basic statistics and coherency in a given table.
        This is a rather strict function. It will fail if any of this conditions are unmet:

        - no reference system is set (st_srid=-1);
        - no homogeneous reference system found (geometries with different reference systems
          present);
        - no homogeneous geometry types found (geometries with different geometry types
          present).

        If this conditions are met, it returns a dictionary with the following keys:

        - xmin: st_xmin of the whole geometry set;
        - xmax: st_xmax of the whole geometry set;
        - ymin: st_ymin of the whole geometry set;
        - ymax: st_ymax of the whole geometry set;
        - srid: homogeneous SRID found as per st_srid;
        - type: homogeneous geometry type found as per st_geometrytype.

        This function is just a convenience wrapper around the more general
        analyzeGeomColumnFromSql.
        
        :param sql: SQL query to work on.
        :type sql: String
        :param geomColumn: Geometry column in the SQL to analyze.
        :type geomColumn: String
        :return: A Dict with basic data about the geometry column.
        :rtype: Dict
        """

        sql = "select * from %s.%s" % (schema, table)

        return self.analyzeGeomColumnFromSql(sql, geomColumn)
    

    def analyzeGeomColumnFromSql(self, sql, geomColumn):
        """
        Analyzes a geometry column for basic statistics and coherency in a given SQL query.
        This is a rather strict function. It will fail if any of this conditions are unmet:

        - no reference system is set (st_srid=-1);
        - no homogeneous reference system found (geometries with different reference systems
          present);
        - no homogeneous geometry types found (geometries with different geometry types
          present).

        If this conditions are met, it returns a dictionary with the following keys:

        - xmin: st_xmin of the whole geometry set;
        - xmax: st_xmax of the whole geometry set;
        - ymin: st_ymin of the whole geometry set;
        - ymax: st_ymax of the whole geometry set;
        - srid: homogeneous SRID found as per st_srid;
        - type: homogeneous geometry type found as per st_geometrytype.

        :param sql: SQL query to work on.
        :type sql: String
        :param geomColumn: Geometry column in the SQL to analyze.
        :type geomColumn: String
        :return: A Dict with basic data about the geometry column.
        :rtype: Dict
        """

        out = {}

        # Analyze geometry column (check SRID and geometry type)
        qsql = """
        select distinct
        st_srid(%s),
        st_geometrytype(%s)
        from
        (%s) a
        """

        cur = self._conn.cursor()
        cur.execute(qsql, (AsIs(geomColumn), AsIs(geomColumn), AsIs(sql)))
        res = cur.fetchall()
        
        if len(res)>1:
            raise PostGisException("Not homogeneous SRID or geometry type: %s." % res)
        elif len(res)==0:
            raise PostGisException("geom column %s seems to be empty." % geomColumn)
        else:
            out["srid"] = res[0][0]
            out["type"] = res[0][1]
            
        # Check extends
        qsql = """
        select
        min(st_xmin(%s)),
        max(st_xmax(%s)),
        min(st_ymin(%s)),
        max(st_ymax(%s))
        from
        (%s) a;
        """

        cur.execute(qsql, (AsIs(geomColumn), AsIs(geomColumn), AsIs(geomColumn), \
                    AsIs(geomColumn), AsIs(sql)))
        res = cur.fetchall()
        cur.close()

        out["xmin"] = res[0][0]
        out["xmax"] = res[0][1]
        out["ymin"] = res[0][2]
        out["ymax"] = res[0][3]

        return out

        
    def getPgDataTypes(self):
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
