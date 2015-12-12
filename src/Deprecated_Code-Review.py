


                

        
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
