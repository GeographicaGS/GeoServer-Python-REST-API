"""
Philosophy: get certain, small information of objects, make a single
call and store the information in members. For example, when created,
GeoServerInstance caches the list of available workspaces in a member.
There is a function called 'refreshWorkspaces()' that refreshes this
list. This minimizes REST calls for minial things to the server.
"""

import requests, json

class GsInstance(object):
    url = None
    adminUser = None
    adminPass = None
    workspaces = None
    settings = None
    contact = None
    layers = None
            
    def __init__(self, url, adminUser, adminPass):
        self.url = url
        self.adminUser = adminUser
        self.adminPass = adminPass
        self.refresh()

    def refresh(self):
        self.settings = requests.get(self.url+"/rest/settings.json", \
                                     auth=(self.adminUser, self.adminPass), \
                                     headers={"Accept": "text/json"}).json()

        self.contact = requests.get(self.url+"/rest/settings/contact.json", \
                                    auth=(self.adminUser, self.adminPass), \
                                    headers={"Accept": "text/json"}).json()
                                             
        workspaces = requests.get(self.url+"/rest/workspaces.json", \
                                  auth=(self.adminUser, self.adminPass), \
                                  headers={"Accept": "text/json"}).json()
                                                                                
        layers = requests.get(self.url+"/rest/layers.json", \
                              auth=(self.adminUser, self.adminPass), \
                              headers={"Accept": "text/json"}).json()
                              
        self.workspaces = {w["name"]:w["href"] for w in workspaces["workspaces"]["workspace"]} \
            if workspaces["workspaces"]<>"" else []
        self.layers = {l["name"]:l["href"] for l in layers["layers"]["layer"]} \
            if layers["layers"]<>"" else []

    def putSettings(self):
        """Puts settings to the server by REST."""
        return requests.put(self.url+"/rest/settings.json", \
                            auth=(self.adminUser, self.adminPass), \
                            headers={"Content-type": "text/json"}, \
                            data=json.dumps(self.settings))

    def putContact(self):
        """Puts contact to the server by REST."""
        return requests.put(self.url+"/rest/settings/contact.json", \
                            auth=(self.adminUser, self.adminPass), \
                            headers={"Content-type": "text/json"}, \
                            data=json.dumps(self.contact))
        
    def writeToJson(self, destination="./", fileNames=["GsInstanceSettings", "GsInstanceContact"]):
        """Writes settings and contact to files."""
        # Disable data item "metadata". It is buggy to redeploy
        toWrite = self.settings
        
        if "metadata" in toWrite["global"]["settings"]:
            del toWrite["global"]["settings"]["metadata"]
        
        f = open(destination+fileNames[0], "w")
        f.write(json.dumps(toWrite, sort_keys=True, indent=4, separators=(",",": ")))
        f.close()

        f = open(destination+fileNames[1], "w")
        f.write(json.dumps(self.contact, sort_keys=True, indent=4, separators=(",",": ")))
        f.close()

    def readFromJson(self, destination="./", fileNames=["GsInstanceSettings", "GsInstanceContact"]):
        """Reads settings and contact from files."""
        f = open(destination+fileNames[0], "r")
        self.settings = json.loads(f.read())
        f.close()
        
        f = open(destination+fileNames[1], "r")
        self.contact = json.loads(f.read())
        f.close()
        
    def getWorkspaceNames(self):
        return self.workspaces.keys()
                                       
    def getLayerNames(self):
        return self.layers.keys()


class GsLayer(object):
    name = None
    url = None
    gsInstance = None
    attribution = None
    defaultStyle = None
    resource = None
    info = None
    type = None
    featureType = None
    
    def __init__(self, url, gsInstance):
        self.gsInstance = gsInstance
        self.url = url
        self.refresh()

    def refresh(self):
        info = requests.get(self.url, \
                            auth=(self.gsInstance.adminUser, \
                                  self.gsInstance.adminPass), \
                            headers={"Accept": "text/json"}).json()["layer"]
        self.info = info
        self.attribution = info["attribution"]
        self.name = info["name"]
        self.defaultStyle = info["defaultStyle"]
        self.resource = info["resource"]
        self.featureType = self.resource["href"]
        self.type = info["type"]

                
class GsWorkspace(object):
    name = None
    url = None
    gsInstance = None
    dataStores = None
    wmsStores = None
    coverageStores = None
    settings = None
    workspaceRoot = None
    info = None

    def __init__(self, url, gsInstance):
        self.url = url
        self.gsInstance = gsInstance
        self.refresh()

    def refresh(self):
        self.info = requests.get(self.url, \
                                 auth=(self.gsInstance.adminUser, \
                                       self.gsInstance.adminPass), \
                                 headers={"Accept": "text/json"}).json()
        self.workspaceRoot = self.info.keys()[0]
        values = self.info.values()[0]
        self.name = values["name"]
        self.dataStores = values["dataStores"]
        self.wmsStores = values["wmsStores"]
        self.coverageStores = values["coverageStores"]
        settings = requests.get(self.url+"/settings.json", \
                                auth=("admin", "geoserver"), \
                                headers={"Accept": "text/json"})
        self.settings = settings.json() if settings.status_code<>401 else None


class GsDataStore(object):
    url = None
    gsInstance = None
    storeTypeRoot = None
    description = None
    default = None
    enabled = None
    info = None
    storeType = None
    itemsUrl = None
    connectionParameters = None
    items = None
    name = None
    workspace = None

    def __init__(self, url, gsInstance):
        self.url = url
        self.gsInstance = gsInstance
        self.refresh()
        
    def refresh(self):
        self.info = requests.get(self.url, \
                                 auth=(self.gsInstance.adminUser, \
                                       self.gsInstance.adminPass), \
                                 headers={"Accept": "text/json"}).json() \

        self.storeTypeRoot = self.info.keys()[0]
        values = self.info.values()[0]
        self.itemsUrl = values["featureTypes"] \
          if self.storeTypeRoot=="dataStore" \
          else values["coverages"]
        self.name = values["name"]
        self.enabled = values["enabled"]
        self.workspace = values["workspace"]
        self.default = values["_default"]
        self.storeType = values["type"]
        self.description = values["description"] if "description" in values.keys() \
          else None
                  
        self.connectionParameters = \
          {i["@key"]: i["$"] for i in values["connectionParameters"]["entry"]} \
          if self.storeTypeRoot=="dataStore" else None
                
        self.items = requests.get(self.itemsUrl, \
                                  auth=(self.gsInstance.adminUser, \
                                        self.gsInstance.adminPass), \
                                  headers={"Accept": "text/json"}).json()
            

class GsFeatureType(object):
    gsInstance = None
    name = None
    url = None
    nativeName = None
    featureTypeType = None
    featureTypeSubtype = None
    info = None
    title = None
    store = None
    metadata = None
    metadataKeys = None
    
    def __init__(self, url, gsInstance):
        self.url = url
        self.gsInstance = gsInstance
        self.metadata = {}
        self.refresh()
        
    def refresh(self):
        self.info = requests.get(self.url, \
                                 auth=(self.gsInstance.adminUser, \
                                       self.gsInstance.adminPass), \
                                 headers={"Accept": "text/json"}).json()
        self.featureTypeType = self.info.keys()[0]
        value = self.info.values()[0]
        self.name = value["name"]
        self.title = value["title"]
        self.nativeName = value["nativeName"]
        self.store = value["store"]

        if "metadata" in value.keys():
            self.metadata = [value["metadata"]["entry"]] \
                if not isinstance(value["metadata"]["entry"], list) \
                else value["metadata"]["entry"]
            self.metadataKeys = [i["@key"] for i in self.metadata]

        if self.featureTypeType=="featureType":
            if self.metadataKeys is not None:
                if "JDBC_VIRTUAL_TABLE" in self.metadataKeys:
                    self.featureTypeSubtype = "VirtualTable"
                else:
                    self.featureTypeSubtype = "PlainTable"
            else:
                self.featureTypeSubtype = "PlainTable"

    def getVirtualSql(self):
        if self.featureTypeSubtype=="VirtualTable":
            meta = [i for i in self.metadata if i["@key"]=="JDBC_VIRTUAL_TABLE"][0]
            return meta["virtualTable"]["sql"]
        else:
            return None

        
class GsException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "GeoServer REST exception: %s" % (self.value)
