import geoserverapirest as gs
reload(gs)

config = {
    "servers": [
        {
            "url": "http://viv3.cica.es/geoserver",
            "admin_user": "admin_viv3_geos",
            "admin_pass": "delTabUNkeR221"
        }]
}

    


# Basic usage          

gsins = gs.GsInstance("http://localhost:8084/geoserver", "admin", "geoserver")

print "workspace|datastore|layer|type|sql_table|host|schema"

for server in config["servers"]:
    gsins = gs.GsInstance(server["url"], server["admin_user"], \
                          server["admin_pass"])

    for layer,url in gsins.layers.iteritems():
        layer = gs.GsLayer(gsins.layers[layer], gsins)
        featureType = gs.GsFeatureType(layer.featureType, gsins)
        dataStore = gs.GsDataStore(featureType.store["href"], gsins)
        workspace = gs.GsWorkspace(dataStore.workspace["href"], gsins)

        if dataStore.storeType=="PostGIS":
            s = "%s|%s|%s|%s|%s|%s|%s" % ( \
                workspace.name, \
                dataStore.name, \
                layer.name, \
                featureType.featureTypeSubtype, \
                featureType.getVirtualSql().replace("\n\r"," ").replace("\n", " "). \
                replace("\r", " ").replace("\r\n", " ").replace("  ", " "). \
                replace("  ", " ").replace("  "," ") \
                if featureType.getVirtualSql() is not None \
                else featureType.nativeName, \
                dataStore.connectionParameters["host"], \
                dataStore.connectionParameters["schema"] \
                )

            print s.replace(" |","|")
