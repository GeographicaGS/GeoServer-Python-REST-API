#!/usr/bin/env python
# coding=UTF-8


"""
The underlying philosophy of the API is to get small bits of information
of objects, make a single call and store the information in members.
For example, when created, GeoServerInstance caches the list of available
workspaces in a member.  There is a function called 'refreshWorkspaces()'
that refreshes this list. This minimizes REST calls for minial things to the server.
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
        creationXml = '<style><name>%s</name><filename>%s.sld</filename></style>' % \
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
            

# class GsFeatureType(object):
#     gsInstance = None
#     name = None
#     url = None
#     nativeName = None
#     featureTypeType = None
#     featureTypeSubtype = None
#     info = None
#     title = None
#     store = None
#     metadata = None
#     metadataKeys = None
    
#     def __init__(self, url, gsInstance):
#         self.url = url
#         self.gsInstance = gsInstance
#         self.metadata = {}
#         self.refresh()
        
#     def refresh(self):
#         self.info = requests.get(self.url, \
#                                  auth=(self.gsInstance.user, \
#                                        self.gsInstance.passwd), \
#                                  headers={"Accept": "text/json"}).json()
#         self.featureTypeType = self.info.keys()[0]
#         value = self.info.values()[0]
#         self.name = value["name"]
#         self.title = value["title"]
#         self.nativeName = value["nativeName"]
#         self.store = value["store"]

#         if "metadata" in value.keys():
#             self.metadata = [value["metadata"]["entry"]] \
#                 if not isinstance(value["metadata"]["entry"], list) \
#                 else value["metadata"]["entry"]
#             self.metadataKeys = [i["@key"] for i in self.metadata]

#         if self.featureTypeType=="featureType":
#             if self.metadataKeys is not None:
#                 if "JDBC_VIRTUAL_TABLE" in self.metadataKeys:
#                     self.featureTypeSubtype = "VirtualTable"
#                 else:
#                     self.featureTypeSubtype = "PlainTable"
#             else:
#                 self.featureTypeSubtype = "PlainTable"

#     def getVirtualSql(self):
#         if self.featureTypeSubtype=="VirtualTable":
#             meta = [i for i in self.metadata if i["@key"]=="JDBC_VIRTUAL_TABLE"][0]
#             return meta["virtualTable"]["sql"]
#         else:
#             return None



# class GsStyle(object):
#     """
#     Style object.
#     """

#     _name = None
#     """Style name."""
#     _sld = None
#     """Style SLD."""
    
#     def __init__(self, name, sld=None):
#         """
#         A style object.

#         :param name: Style name inside GeoServer.
#         :type name: String
#         :param sld: XML SLD definition for style.
#         :type sld: String

#         .. todo:: validate XML
#         """
#         self._name = name
#         self._sld = sld

#     @property
#     def name(self):
#         """
#         Name of the style.

#         :return: The name of the style.
#         :rtype: String
#         """
#         return self._name

#     @property
#     def sld(self):
#         """
#         XML SLD for the style.

#         :return: The XML SLD for the style.
#         :rtype: String
#         """
#         return self._sld
        
    
    
# class GsException(Exception):
#     def __init__(self, value):
#         self.value = value

#     def __str__(self):
#         return "GeoServer REST exception: %s" % (self.value)



