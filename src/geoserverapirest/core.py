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

import requests, json

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
              {u'@key': u'Expose primary keys', u'$': u'false'},
              {u'@key': u'create database', u'$': u'false'},
              {u'@key': u'preparedStatements', u'$': u'false'},
              {u'@key': u'Estimated extends', u'$': u'false'},
              {u'@key': u'user', u'$': user}]
            },
            u'name': name,
            u'enabled': True,
            u'workspace': {
              u'href': u'http://localhost:8084/geoserver/rest/workspaces/%s.json' % workspace,
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
                            

    def createFeatureTypeFromPostGisTable(self, workspace, datastore, table, name, title):
        """
        Creates a feature type from an existing PostGIS table.

        :param workspace: Name of the workspace the DataStore belongs to.
        :type workspace: String
        :param datastore: Name of the DataStore the FeatureType will be created in.
        :type datastore: String
        :param name: Name of the new FeatureType.
        :type name: String

        .. todo:: change to JSON creation, check get for feature types.
        .. todo:: a lot of items has been purged. Check test_15-Query.py for the full dict response of a get feature type.
        """

        creationDict = \
        {u'featureType':
          {u'circularArcPresent': False,
          u'name': name,
          u'title': title,
          u'enabled': True,
          u'namespace': {
            u'href': u'http://localhost:8084/geoserver/rest/namespaces/%s.json' % workspace,
            u'name': workspace
          },
          u'projectionPolicy': u'FORCE_DECLARED',
          u'numDecimals': 0,
          u'nativeName': table,
          u'maxFeatures': 0,
          u'store': {
            u'href': u'http://localhost:8084/geoserver/rest/workspaces/new_workspace/datastores/%s.json' % datastore,
            u'name': datastore,
            u'@class': u'dataStore'},
          u'overridingServiceSRS': False}}
        
        r = requests.post("%s/rest/workspaces/%s/datastores/%s/featuretypes.json" % \
                          (self.url, workspace, datastore), \
                          auth=(self.user, self.passwd), \
                          headers={"Content-Type": "text/json"}, \
                          data=json.dumps(creationDict))

        import pytest
        pytest.set_trace()
                          
        return r.status_code


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
        """
        
        r = requests.get("%s/rest/workspaces/%s/datastores/%s.json" % \
                         (self.url, workspace, datastore), \
                         auth=(self.user, self.passwd), \
                         headers={"Accept": "text/json"})

        return r.json()






class GsException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "GeoServer REST exception: %s" % (self.value)









                

        
#     # def refresh(self):
#     #     """Will fetch again information regarding settings, contact, workspaces,
#     #     and layers from the instance.

#     #     Deprecate!!!
#     #     """
        
#     #     self.settings = requests.get(self.url+"/rest/settings.json", \
#     #                                  auth=(self.user, self.passwd), \
#     #                                  headers={"Accept": "text/json"}).json()

#     #     self.contact = requests.get(self.url+"/rest/settings/contact.json", \
#     #                                 auth=(self.user, self.passwd), \
#     #                                 headers={"Accept": "text/json"}).json()
                                                                                
#     #     layers = requests.get(self.url+"/rest/layers.json", \
#     #                           auth=(self.user, self.passwd), \
#     #                           headers={"Accept": "text/json"}).json()
                              
#     #     self.workspaces = {w["name"]:w["href"] for w in workspaces["workspaces"]["workspace"]} \
#     #         if workspaces["workspaces"]<>"" else []
#     #     self.layers = {l["name"]:l["href"] for l in layers["layers"]["layer"]} \
#     #         if layers["layers"]<>"" else []

#     # def putSettings(self):
#     #     """Puts settings information to the server by REST."""
        
#     #     return requests.put(self.url+"/rest/settings.json", \
#     #                         auth=(self.user, self.passwd), \
#     #                         headers={"Content-type": "text/json"}, \
#     #                         data=json.dumps(self.settings))

#     # def putContact(self):
#     #     """Puts contact information to the server by REST."""
        
#     #     return requests.put(self.url+"/rest/settings/contact.json", \
#     #                         auth=(self.user, self.passwd), \
#     #                         headers={"Content-type": "text/json"}, \
#     #                         data=json.dumps(self.contact))
        
#     # def writeToJson(self, destination="./", fileNames=["GsInstanceSettings", "GsInstanceContact"]):
#     #     """Writes settings and contact to JSON files.

#     #     :param destination: Destination folder to put the files in. Must end in /.
#     #     :type destination: String
#     #     :param fileNames: Names for settings and contact files, respectively.
#     #     :type fileNames: A list of two strings

#     #     .. todo:: Destination folder may not end in /.
           
#     #     .. todo:: Separate this method in two, one for each file.
#     #     """
        
#     #     # Disable data item "metadata". It is buggy to redeploy
#     #     toWrite = self.settings
        
#     #     if "metadata" in toWrite["global"]["settings"]:
#     #         del toWrite["global"]["settings"]["metadata"]
        
#     #     f = open(destination+fileNames[0], "w")
#     #     f.write(json.dumps(toWrite, sort_keys=True, indent=4, separators=(",",": ")))
#     #     f.close()

#     #     f = open(destination+fileNames[1], "w")
#     #     f.write(json.dumps(self.contact, sort_keys=True, indent=4, separators=(",",": ")))
#     #     f.close()

#     # def readFromJson(self, destination="./", fileNames=["GsInstanceSettings", "GsInstanceContact"]):
#     #     """Reads settings and contact from JSON files.

#     #     :param destination: Source folder to read files from. May end in /.
#     #     :type destination: String
#     #     :param fileNames: File names for files.
#     #     :type fileNames: A list of two strings

#     #     .. todo:: Destination folder may not end in /.
           
#     #     .. todo:: Separate this method in two, one for each file.
#     #     """
#     #     f = open(destination+fileNames[0], "r")
#     #     self.settings = json.loads(f.read())
#     #     f.close()
        
#     #     f = open(destination+fileNames[1], "r")
#     #     self.contact = json.loads(f.read())
#     #     f.close()
        
#     # def getWorkspaceNames(self):
#     #     """Returns a list with workspace names.

#     #     :return: A list with workspace names.
#     #     :rtype: List
#     #     """

#     #     workspaces = requests.get(self.url+"/rest/workspaces.json", \
#     #                               auth=(self.user, self.passwd), \
#     #                               headers={"Accept": "text/json"}).json()["workspaces"]["workspace"]

                
#     #     return [i["name"] for i in workspaces]

#     # def getWorkspace(self, name):
#     #     """Returns a GsWorkspace"""
#     #     pass
                                           
#     # def getLayerNames(self):
#     #     """Returns a list with layer names.

#     #     :return: A list with layer names.
#     #     :rtype: List
#     #     """

#     #     return self.layers.keys()



        
        


        
#     # def getStyleSld(self, name):
#     #     """Returns the SLD as a string of a given style.

#     #     :param name: Name of the style.
#     #     :type name: String
#     #     :return: a string containing the XML SLD definition of the style
#     #     :rtype: String

#     #     .. todo:: Create funtions to get styles in a Workspace (in the workspace class)
#     #     """
        
#     #     r = requests.get("%s/rest/styles/%s.sld" % (self.url, name), \
#     #                      auth=(self.user, self.passwd), \
#     #                      headers={"Accept": "text/xml"}).content

#     #     return r

#     # def createWorkspace(self, name):
#     #     """Creates a new workspace.

#     #     :param name: Name of the new workspace.
#     #     :type name: String

#     #     .. todo:: handle return type.
#     #     """
#     #     r = requests.get

            
# class GsLayer(object):
#     """
#     Layer object.
#     """
#     _name = None
#     """Layer name."""
    
#     # _url = None
#     # attribution = None
#     # defaultStyle = None
#     # resource = None
#     # info = None
#     # type = None
#     # featureType = None
    
#     def __init__(self, name):
#         """
#         Defines a layer.

#         :param name: Layer's name.
#         :type name: String
#         """
#         self._name = name

#     @property
#     def name(self):
#         """
#         Name of layer.

#         :return: Name of layer.
#         :rtype: String
#         """
#         return self._name
    
    
#     # def refresh(self):
#     #     info = requests.get(self.url, \
#     #                         auth=(self.gsInstance.user, \
#     #                               self.gsInstance.passwd), \
#     #                         headers={"Accept": "text/json"}).json()["layer"]
#     #     self.info = info
#     #     self.attribution = info["attribution"]
#     #     self.name = info["name"]
#     #     self.defaultStyle = info["defaultStyle"]
#     #     self.resource = info["resource"]
#     #     self.featureType = self.resource["href"]
#     #     self.type = info["type"]

                
# class GsWorkspace(object):
#     """
#     Workspace object.
#     """
        
#     _name = None
#     """Workspace style."""
#     # url = None
#     # gsInstance = None
#     # dataStores = None
#     # wmsStores = None
#     # coverageStores = None
#     # settings = None
#     # workspaceRoot = None
#     # info = None

#     def __init__(self, name):
#         """
#         A Workspace object.

#         :param name: 
#         self.url = url
#         self.gsInstance = gsInstance
#         # self.refresh()

#     def refresh(self):
#         self.info = requests.get(self.url, \
#                                  auth=(self.gsInstance.user, \
#                                        self.gsInstance.passwd), \
#                                  headers={"Accept": "text/json"}).json()
#         self.workspaceRoot = self.info.keys()[0]
#         values = self.info.values()[0]
#         self.name = values["name"]
#         self.dataStores = values["dataStores"]
#         self.wmsStores = values["wmsStores"]
#         self.coverageStores = values["coverageStores"]
#         settings = requests.get(self.url+"/settings.json", \
#                                 auth=("admin", "geoserver"), \
#                                 headers={"Accept": "text/json"})
#         self.settings = settings.json() if settings.status_code<>401 else None


# class GsDataStore(object):
#     url = None
#     gsInstance = None
#     storeTypeRoot = None
#     description = None
#     default = None
#     enabled = None
#     info = None
#     storeType = None
#     itemsUrl = None
#     connectionParameters = None
#     items = None
#     name = None
#     workspace = None

#     def __init__(self, url, gsInstance):
#         self.url = url
#         self.gsInstance = gsInstance
#         self.refresh()
        
#     def refresh(self):
#         self.info = requests.get(self.url, \
#                                  auth=(self.gsInstance.user, \
#                                        self.gsInstance.passwd), \
#                                  headers={"Accept": "text/json"}).json() \

#         self.storeTypeRoot = self.info.keys()[0]
#         values = self.info.values()[0]
#         self.itemsUrl = values["featureTypes"] \
#           if self.storeTypeRoot=="dataStore" \
#           else values["coverages"]
#         self.name = values["name"]
#         self.enabled = values["enabled"]
#         self.workspace = values["workspace"]
#         self.default = values["_default"]
#         self.storeType = values["type"]
#         self.description = values["description"] if "description" in values.keys() \
#           else None
                  
#         self.connectionParameters = \
#           {i["@key"]: i["$"] for i in values["connectionParameters"]["entry"]} \
#           if self.storeTypeRoot=="dataStore" else None
                
#         self.items = requests.get(self.itemsUrl, \
#                                   auth=(self.gsInstance.user, \
#                                         self.gsInstance.passwd), \
#                                   headers={"Accept": "text/json"}).json()
