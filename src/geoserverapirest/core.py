#!/usr/bin/env python
# coding=UTF-8


"""
The underlying philosophy of the API is to get small bits of information
of objects, make a single call and store the information in members.
For example, when created, GeoServerInstance caches the list of available
workspaces in a member.  There is a function called 'refreshWorkspaces()'
that refreshes this list. This minimizes REST calls for minial things to the server.

^^^Deprecate, rewrite 
"""

import requests, json, ext.postgis, ext.const

class GsInstance(object):
    """
    This class represents a top level GeoServer instance.

    .. todo:: do not restrict access only to the admin user.
    """
    
    _url = None
    """URL of the GeoServer."""
    _user = None
    """Administration user of GeoServer."""
    _passwd = None
    """Password for administration user of GeoServer."""

        
    def __init__(self, url, user="admin", passwd="geoserver"):
        """
        The constructor will fetch automatically initial information
        from the GeoServer concerning settings, contact, workspaces,
        and layers and will store this info in members.

        :param url: URL of GeoServer to connect to.
        :type url: String
        :param user: Administration user name.
        :type user: String
        :param passwd: Administration user password.
        :type passwd: String
        """
        self._url = url
        self._user = user
        self._passwd = passwd

        
    @property
    def url(self):
        """
        Returns the URL of the GeoServer instance.

        :return: The URL of the GeoServer instance.
        :rtype: String
        """
        return self._url

    
    @property
    def user(self):
        """
        Returns the name of the admin user.

        :return: The name of the user.
        :rtype: String
        """
        return self._user

    
    @property
    def passwd(self):
        """
        Returns the password of the admin user.

        :return: The password of the user.
        :rtype: String
        """
        return self._passwd

    
    def checkAlive(self):
        """
        Checks if the instance is alive by checking access to settings.

        Returns connection code:
        - 404: URL not found or not a GeoServer
        - 200: success, it seems to be a GeoServer
        """
        try:
            r = requests.get("%s/rest/settings.json" % self._url, \
                            auth=(self._user, self._passwd), \
                            headers={"Accept": "text/json"}).json()

            return 200 if "global" in r.keys() else 404
        except:
            return 404

        
    def getStyleNames(self):
        """
        Returns a list with style names.

        :return: A list with style names.
        :rtype: List
        """
        r = requests.get("%s/rest/styles.json" % self._url, \
                            auth=(self._user, self._passwd), \
                            headers={"Accept": "text/json"}).json()["styles"]["style"]
        return [i["name"] for i in r]

    
    def createStyle(self, name, sld):
        """
        Generates the given style at instance level.

        :param name: The new style name.
        :type name: String
        :param sld: The XML SLD style definition.
        :type sld: String

        .. todo:: Manage return codes
        """
        creationXml = "<style><name>%s</name><filename>%s.sld</filename></style>" % \
          (name, name)
        
        r = requests.post("%s/rest/styles.sld" % (self.url), \
                          params={"name": name}, \
                          auth=(self.user, self.passwd), \
                          headers={"Content-Type": "application/xml"}, \
                          data=creationXml)

        r = requests.put("%s/rest/styles/%s" % (self.url, name), \
                         params={"raw": True}, \
                         auth=(self.user, self.passwd), \
                         headers={"Content-Type": "application/vnd.ogc.sld+xml"}, \
                         data=sld)

        return r.status_code

    
    def deleteStyle(self, name):
        """
        Deletes a style.

        :param name: The name of the style to be deleted.
        :type name: String

        .. todo:: check return types
        """
        
        r = requests.delete("%s/rest/styles/%s" % (self.url, name), \
                            params={"purge": True}, \
                            auth=(self.user, self.passwd))

        return r.status_code


    def getWorkspaceNames(self):
        """
        Returns a list with workspace names.

        :return: A list with workspace names.
        :rtype: List

        .. todo:: check return types
        """
        r = requests.get("%s/rest/workspaces.json" % self._url, \
                         auth=(self._user, self._passwd), \
                         headers={"Accept": "text/json"}).json()["workspaces"]
        
        if r=="":
            return []
        else:
            return [i["name"] for i in r["workspace"]]

    
    def createWorkspace(self, name):
        """
        Creates a workspace.

        :param name: The name of the workspace to be created.
        :type name: String

        .. todo:: check return types
        """
        creationXml = "<workspace><name>%s</name></workspace>" % name
        r = requests.post("%s/rest/workspaces.xml" % (self.url), \
                            auth=(self.user, self.passwd), \
                            headers={"Content-Type": "application/xml"}, \
                            data=creationXml)
        return r.status_code


    def deleteWorkspace(self, name, recursive=False):
        """
        Deletes a workspace.

        :param name: The name of the workspace to be deleted.
        :type name: String

        .. todo:: check return types
        """
        r = requests.delete("%s/rest/workspaces/%s" % (self.url, name), \
                            params={"recurse": recursive}, \
                            auth=(self.user, self.passwd))
        return r.status_code


    def getNamespaceNames(self):
        """
        Returns a list with existing namespace names.

        :return: List with existing namespace names.
        :rtype: List

        .. todo:: handle return types

        .. todo:: run tests with a full empty GeoServer
        """
        r = requests.get("%s/rest/namespaces.json" % self.url, \
                         auth=(self.user, self.passwd)).json()

        if r["namespaces"]=="":
            return []
        else:
            return [i["name"] for i in r["namespaces"]["namespace"]]


    def createPostGisDataStore(self, workspace, name, host, port, user, passwd, \
                               database, schema):
        """
        Creates a new PostGIS datastore in a given workspace.

        :param workspace: Name of the workspace to create the datastore into.
        :type workspace: String
        :param name: Name for the new datastore.
        :type name: String
        :param host: Host of the PostGIS.
        :type host: String
        :param port: Port of the PostGIS.
        :type port: String
        :param user: User of the PostGIS.
        :type user: String
        :param passwd: Password of the PostGIS.
        :type passwd: String
        :param database: Database to connect to.
        :type database: String

        .. todo:: Check return codes.
        .. todo:: A lot of options left on default. Configure.
        """
        creationDict = \
        {u'dataStore':
          {u'connectionParameters':
            {u'entry': [
              {u'@key': u'port', u'$': port},
              {u'@key': u'passwd', u'$': passwd},
              {u'@key': u'dbtype', u'$': u'postgis'},
              {u'@key': u'host', u'$': host},
              {u'@key': u'encode functions', u'$': u'false'},
              {u'@key': u'validate connections', u'$': u'false'},
              {u'@key': u'Support on the fly geometry simplification', u'$': u'false'},
              {u'@key': u'database', u'$': database},
              {u'@key': u'namespace', u'$': u'http://%s' % workspace},
              {u'@key': u'schema', u'$': schema},
              {u'@key': u'Test while idle', u'$': u'false'},
              {u'@key': u'Loose bbox', u'$': u'false'},
              {u'@key': u'Expose primary keys', u'$': u'true'},
              {u'@key': u'create database', u'$': u'false'},
              {u'@key': u'preparedStatements', u'$': u'false'},
              {u'@key': u'Estimated extends', u'$': u'false'},
              {u'@key': u'user', u'$': user}]
            },
            u'name': name,
            u'enabled': True,
            u'workspace': {
              u'href': u'http://%s/geoserver/rest/workspaces/%s.json' % (self.url, workspace),
              u'name': workspace
            },
            u'_default': False,
            u'type': u'PostGIS'}}

        r = requests.post("%s/rest/workspaces/%s/datastores.json" % (self.url, workspace), \
                          auth=(self.user, self.passwd), \
                          headers={"Content-Type": "text/json"}, \
                          data=json.dumps(creationDict))
                          
        return r.status_code


    def deleteDatastore(self, workspace, name):
        """
        Deletes a DataStore by workspace and name.

        :param workspace: Name of the workspace the DataStore belongs to.
        :type workspace: String
        :param name: Name of the DataStore to be deleted.
        :type name: String

        .. todo: check for additional parameters.
        """
        r = requests.delete("%s/rest/workspaces/%s/datastores/%s" % \
                            (self.url, workspace, name), \
                            auth=(self.user, self.passwd))
        return r.status_code
                            

    def createFeatureTypeFromPostGisTable(self, workspace, datastore, table, name, title, \
                                          pgpassword, srs, nativeCRS=None):
        """
        Creates a feature type from an existing PostGIS table.
        ONLY SUPPORTS SINGLE GEOM TABLES BY NOW.

        :param workspace: Name of the workspace the DataStore belongs to.
        :type workspace: String
        :param datastore: Name of the DataStore the FeatureType will be created in.
        :type datastore: String
        :param table: Name of the source table, without schema (schema is specified in the datastore).
        :type table: String
        :param name: Name of the new FeatureType.
        :type name: String
        :param title: Title of the new Feature Type.
        :type title: String
        :param pgpassword: Password for the PostGIS the DataStore references. This is so because we can't get the password from the GeoServer DataStore yet.
        :type pgpassword: String
        :param srs: Declared SRS. The default SRS the layer will be served on. Must be in the form "EPSG:XXXXX"
        :type srs: String
        :param nativeCRS: Native CRS EPSG. Defaults to None. Has to be explicitly given. In the future, if None, will be infered from PostGIS somehow. Must be in the form "EPSG:XXXXX"
        :type nativeCRS: String

        .. todo:: Change to JSON creation, check get for feature types.
        .. todo:: A lot of items has been purged. Check test_15-Query.py for the full dict response of a get feature type.
        .. todo:: try to get the DataStore connection password from GeoServer.
        .. todo:: support multigeom tables.
        .. todo:: Infere EPSG from geometries or PostGIS geometry_columns.
        """

        creationDict = \
        {u'featureType':
          {u'circularArcPresent': False,
          u'name': name,
          u'title': title,
          u'enabled': True,
          u'namespace': {
            u'href': u'http://%s/geoserver/rest/namespaces/%s.json' % (self.url, workspace),
            u'name': workspace
          },
          u'projectionPolicy': u'FORCE_DECLARED',
          u'numDecimals': 0,
          u'nativeName': table,
          u'maxFeatures': 0,
          u'store': {
            u'href': u'http://%s/geoserver/rest/workspaces/%s/datastores/%s.json' % (self.url, workspace, datastore),
            u'name': datastore,
            u'@class': u'dataStore'},
          u'overridingServiceSRS': False}}

        # Get datastore data
        ds = self.getConnDataFromPostGisDataStore(workspace, datastore)
        
        # Add attributes
        pgi = ext.postgis.GsPostGis(ds["host"], ds["port"], ds["database"], ds["user"], pgpassword)

        creationDict["featureType"]["attributes"] = pgi.getFieldsFromTable(ds["schema"], table)["attributes"]
        pgi.close()
        
        creationDict["featureType"]["nativeCRS"] = ext.const.epsg["EPSG:%s" % nativeCRS]
        creationDict["featureType"]["srs"] = "EPSG:%s" % srs
        
        r = requests.post("%s/rest/workspaces/%s/datastores/%s/featuretypes.json" % \
                          (self.url, workspace, datastore), \
                          auth=(self.user, self.passwd), \
                          headers={"Content-Type": "text/json"}, \
                          data=json.dumps(creationDict))
                                                    
        return r.status_code


    def createFeatureTypeFromPostGisQuery(self, workspace, datastore, sql, keyColumn, geomColumn, \
                                          geomType, name, title, pgpassword, srs, nativeCRS=None):
        """
        Creates a Feature Type from a query to a PostGIS.

        :param workspace: Name of the workspace the DataStore belongs to.
        :type workspace: String
        :param datastore: Name of the DataStore the FeatureType will be created in.
        :type datastore: String
        :param sql: SQL to create the Feature Type.
        :type sql: String
        :param keyColumn: Name of the primary key column.
        :type 
        :param geomColumn: Name of the geometry column in the SQL.
        :type geomColumn: String
        :param geomType: Type of the geometry column in the SQL. Can be Polygon, MultiPolygon ...
        :type geomType: String
        :param name: Name of the new FeatureType.
        :type name: String
        :param title: Title of the new Feature Type.
        :type title: String
        :param pgpassword: Password for the PostGIS the DataStore references. This is so because we can't get the password from the GeoServer DataStore yet.
        :type pgpassword: String
        :param srs: Declared SRS. The default SRS the layer will be served on. Must be as the EPSG code alone.
        :type srs: String
        :param nativeCRS: Native CRS EPSG. Defaults to None. Has to be explicitly given. In the future, if None, will be infered from PostGIS somehow. Must be as the EPSG code alone.
        :type nativeCRS: String

        .. todo:: Change to JSON creation, check get for feature types.
        .. todo:: A lot of items has been purged. Check test_15-Query.py for the full dict response of a get feature type.
        .. todo:: try to get the DataStore connection password from GeoServer.
        .. todo:: support multigeom tables.
        .. todo:: Infere EPSG from geometries or PostGIS geometry_columns.
        .. todo:: check all available geomType.
        """




#        {u'featureType':
#         {u'circularArcPresent': False,

                   # u'nativeBoundingBox': {u'minx': 102471.570069193, u'miny': 3987969.4688624, u'maxx': 619151.299977792, u'maxy': 4274175.62512184, u'crs': {u'$': u'EPSG:25830', u'@class': u'projected'}}

         # , u'nativeCRS': {u'$': u'PROJCS["ETRS89 / UTM zone 30N", \n  GEOGCS["ETRS89", \n    DATUM["European Terrestrial Reference System 1989", \n      SPHEROID["GRS 1980", 6378137.0, 298.257222101, AUTHORITY["EPSG","7019"]], \n      TOWGS84[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], \n      AUTHORITY["EPSG","6258"]], \n    PRIMEM["Greenwich", 0.0, AUTHORITY["EPSG","8901"]], \n    UNIT["degree", 0.017453292519943295], \n    AXIS["Geodetic longitude", EAST], \n    AXIS["Geodetic latitude", NORTH], \n    AUTHORITY["EPSG","4258"]], \n  PROJECTION["Transverse_Mercator", AUTHORITY["EPSG","9807"]], \n  PARAMETER["central_meridian", -3.0], \n  PARAMETER["latitude_of_origin", 0.0], \n  PARAMETER["scale_factor", 0.9996], \n  PARAMETER["false_easting", 500000.0], \n  PARAMETER["false_northing", 0.0], \n  UNIT["m", 1.0], \n  AXIS["Easting", EAST], \n  AXIS["Northing", NORTH], \n  AUTHORITY["EPSG","25830"]]', u'@class': u'projected'}

         # , u'name': u'mvw',

         # u'title': u'mvw',

         # u'latLonBoundingBox': {u'minx': -7.559552224805082, u'miny': 35.95523005749738, u'maxx': -1.631534162160534, u'maxy': 38.6160383053748, u'crs': u'GEOGCS["WGS84(DD)", \n  DATUM["WGS84", \n    SPHEROID["WGS84", 6378137.0, 298.257223563]], \n  PRIMEM["Greenwich", 0.0], \n  UNIT["degree", 0.017453292519943295], \n  AXIS["Geodetic longitude", EAST], \n  AXIS["Geodetic latitude", NORTH]]'}

         # , u'enabled': True,

         # u'namespace': {u'href': u'http://sourcegeoserver:8080/geoserver/rest/namespaces/new_workspace.json', u'name': u'new_workspace'}

         # , u'projectionPolicy': u'FORCE_DECLARED',

         # u'numDecimals': 0,

         # u'srs': u'EPSG:25830',

         # u'overridingServiceSRS': False,

         # u'keywords': {u'string': [u'mvw', u'features']},

         # u'attributes':
         # {u'attribute': [
         #     {u'maxOccurs': 1, u'nillable': True, u'binding': u'java.lang.Long', u'name': u'gid', u'minOccurs': 0},
         #     {u'maxOccurs': 1, u'nillable': True, u'binding': u'java.lang.String', u'name': u'grd_fixid', u'minOccurs': 0},
         #     {u'maxOccurs': 1, u'nillable': True, u'binding': u'java.lang.String', u'name': u'grd_floaid', u'minOccurs': 0},
         #     {u'maxOccurs': 1, u'nillable': True, u'binding': u'java.lang.String', u'name': u'grd_inspir', u'minOccurs': 0},
         #     {u'maxOccurs': 1, u'nillable': True, u'binding': u'java.math.BigDecimal', u'name': u'n_hogares', u'minOccurs': 0},
         #     {u'maxOccurs': 1, u'nillable': True, u'binding': u'com.vividsolutions.jts.geom.Polygon', u'name': u'geom', u'minOccurs': 0}]}

         # , u'nativeName': u'mvw',
         # u'maxFeatures': 0,
         # u'store': {u'href': u'http://sourcegeoserver:8080/geoserver/rest/workspaces/new_workspace/datastores/viv3.json', u'name': u'viv3', u'@class': u'dataStore'},

         # u'metadata': {
         #     u'entry':
         #     [
         #         {u'@key': u'cachingEnabled', u'$': u'false'},
         #     {u'@key': u'JDBC_VIRTUAL_TABLE', u'virtualTable':
         #      {u'geometry':
         #       {u'srid': 25830, u'type': u'Polygon', u'name': u'geom'},
         #      u'keyColumn': u'gid',
         #      u'name': u'mvw',
         #      u'escapeSql': False,
         #      u'sql': u'select * from\r\nregistro_longitudinal_20150330.mvw__hogares_250\n'}}]}}}



                 
        creationDict = \
        {u'featureType':
          {u'circularArcPresent': False,
          u'name': name,
          u'title': title,
          u'enabled': True,
          u'namespace': {
            u'href': u'http://%s/geoserver/rest/namespaces/%s.json' % (self.url, workspace),
            u'name': workspace
          },
          u'projectionPolicy': u'FORCE_DECLARED',
          u'numDecimals': 0,
          u'nativeName': name,
          u'maxFeatures': 0,
          u'store': {
            u'href': u'http://%s/geoserver/rest/workspaces/%s/datastores/%s.json' % (self.url, workspace, datastore),
            u'name': datastore,
            u'@class': u'dataStore'},
          u'overridingServiceSRS': False}}

        # Get datastore data
        ds = self.getConnDataFromPostGisDataStore(workspace, datastore)
        
        # Add attributes
        pgi = ext.postgis.GsPostGis(ds["host"], ds["port"], ds["database"], ds["user"], pgpassword)

        creationDict["featureType"]["attributes"] = pgi.getFieldsFromSql(sql, geomColumn, geomType) \
          ["attributes"]
          
        pgi.close()
        creationDict["featureType"]["nativeCRS"] = ext.const.epsg["EPSG:%s" % nativeCRS]
        creationDict["featureType"]["srs"] = "EPSG:%s" % srs

        creationDict["featureType"]["metadata"] = {
            u'entry': [
                {u'@key': u'cachingEnabled', u'$': u'false'},
                {u'@key': u'JDBC_VIRTUAL_TABLE', u'virtualTable': {
                    u'name': name,
                    u'geometry': {u'srid': srs, u'type': geomType, u'name': geomColumn},
                    u'keyColumn': keyColumn,
                    u'escapeSql': False,
                    u'sql': sql}}]}

        r = requests.post("%s/rest/workspaces/%s/datastores/%s/featuretypes.json" % \
                          (self.url, workspace, datastore), \
                          auth=(self.user, self.passwd), \
                          headers={"Content-Type": "text/json"}, \
                          data=json.dumps(creationDict))


        import pytest
        pytest.set_trace()
                          
        return r.status_code
    

    def getConnDataFromPostGisDataStore(self, workspace, datastore):
        """
        Returns a dictionary with connection info for the given PostGIS DataStore.

        It can't return yet the password.

        :param workspace: Workspace name.
        :type workspace: String
        :param datastore: DataStore name.
        :type datastore: String

        .. todo:: Make test for retrieving information from an empty GeoServer.
        .. todo:: Make test for retrieving information from a shut down GeoServer.
        .. todo:: Enable at GsInstance level a cache to store PostGIS DataStore passwords.
        .. todo:: Check if not a PostGIS DataStore.
        """

        r = self.getDataStore(workspace, datastore)["dataStore"]["connectionParameters"]["entry"]

        out = \
          {"port": self._getAmpKey(r, "port"),
           "host": self._getAmpKey(r, "host"),
           "database": self._getAmpKey(r, "database"),
           "schema": self._getAmpKey(r, "schema"),
           "user": self._getAmpKey(r, "user")}
        
        return out
    
    
    def getDataStoreNames(self, workspace):
        """
        Returns the list of names of DataStores available for a workspace.

        :param workspace: Name of the workspace to search.
        :type workspace: String
        """

        r = requests.get("%s/rest/workspaces/%s/datastores.json" % \
                         (self.url, workspace), \
                         auth=(self.user, self.passwd), \
                         headers={"Accept": "text/json"}).json()

        if r["dataStores"]=="":
            return []
        else:
            return [i["name"] for i in r["dataStores"]["dataStore"]]
    

    def getFeatureTypesNames(self, workspace, datastore):
        """
        Gets a list with names of Feature Types in a given DataStore and Workspace.

        :param workspace: Name of the workspace.
        :type workspace: String
        :param datastore: Name of the DataStore.
        :type datastore: String

        .. todo:: handle errors in requests
        """
        r = requests.get("%s/rest/workspaces/%s/datastores/%s/featuretypes.json" % \
                         (self.url, workspace, datastore), \
                         auth=(self.user, self.passwd), \
                         headers={"Accept": "text/json"}).json()

        if r["featureTypes"]=="":
            return []
        else:
            return [i["name"] for i in r["featureTypes"]["featureType"]]


    def getFeatureType(self, workspace, datastore, name):
        """
        Gets Dict details of a DataStore.

        :param workspace: Name of the workspace.
        :type workspace: String
        :param datastore: Name of the datastore.
        :type datastore: String
        :param name: Name of the feature type.
        :type name: String

        .. todo:: handle different request answers.
        """
        
        r = requests.get("%s/rest/workspaces/%s/datastores/%s/featuretypes/%s.json" % \
                         (self.url, workspace, datastore, name), \
                         auth=(self.user, self.passwd), \
                         headers={"Accept": "text/json"})

        return r.json()

        
    def getDataStore(self, workspace, datastore):
        """
        Gets Dict details of a DataStore.

        :param workspace: Name of the workspace.
        :type workspace: String
        :param datastore: Name of the datastore.
        :type datastore: String

        .. todo:: handle different request answers.
        .. todo:: document return for all functions.
        """
        
        r = requests.get("%s/rest/workspaces/%s/datastores/%s.json" % \
                         (self.url, workspace, datastore), \
                         auth=(self.user, self.passwd), \
                         headers={"Accept": "text/json"})

        return r.json()


    def deleteFeatureType(self, workspace, datastore, featuretype, recurse=False):
        """
        Deletes a feature type.

        :param workspace: Name of the workspace the feature type belongs to.
        :type workspace: String
        :param datastore: Name of the datastore the feature type belongs to.
        :type datastore: String
        :param featuretype: Name of the feature type.
        :type featuretype: String
        :return: The status code of the delete request.
        :rtype: Integer
        """

        r = requests.delete("%s/rest/workspaces/%s/datastores/%s/featuretypes/%s" % \
                            (self.url, workspace, datastore, featuretype), \
                            params={"recurse": recurse}, \
                            auth=(self.user, self.passwd))

        return r.status_code


    def getLayerNames(self):
        """
        Return a list with layer names.
        """

        r = requests.get("%s/rest/layers.json" % self.url, \
                         auth=(self.user, self.passwd), \
                         headers={"Accept": "text/json"})

        if r.status_code==200:
            r = r.json()
            return [i["name"] for i in r["layers"]["layer"]]
                         

    def getLayer(self, name):
        """
        Returns layer definition.

        :param name: Name of the layer.
        :type name: String
        :return: A JSON with the layer definition.
        :rtype: String
        """

        r = requests.get("%s/rest/layers/%s" % (self.url, name), \
                         auth=(self.user, self.passwd), \
                         headers={"Accept": "text/json"})

        return r.json()


    def updateLayer(self, name, styles=None):
        """
        Updates a layer.

        :param styles: A list with style names to be assigned to the layer.
        :type styles: List
        :return: Code status
        :rtype: Integer

        .. todo:: Add more customizations.
        """

        modification = {"layer": {}}
        
        if styles is not None:
            styleList = []
            
            for i in styles:
                d = {"name": i,
                     "href": "%s/rest/styles/%s.json" % (self.url, i)}
                    
                styleList.append(d)

            s = {"@class": "linked-hash-set",
                 "style": styleList}

            modification["layer"]["styles"] = s
            
        r = requests.put("%s/rest/layers/%s" % (self.url, name), \
                         auth=(self.user, self.passwd), \
                         headers={"Content-Type": "text/json"}, \
                         data=json.dumps(modification))
                         
        return r.status_code
                
        
    def _getAmpKey(self, pairsDictList, key):
        """
        Searchs in a list of Dict pairs in the GeoServer form {"@key": "a", "$": "b"} the
        value of the given key.

        :param pairsDictList: The list of dictionaries containing the key/value pairs.
        :type: List
        :param key: The key to be searched in the "@key" items.
        :type: String
        """

        r = [i["$"] for i in pairsDictList if i["@key"]==key]

        return r[0]

    
                
class GsException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "GeoServer REST exception: %s" % (self.value)





