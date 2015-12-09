import geoserverapirest.core as gs
reload(gs)

# Test for GeoServer cloning
gsinsSource = gs.GsInstance("http://localhost:8084/geoserver", "admin", "geoserver")
gsinsDestination = gs.GsInstance("http://localhost:8085/geoserver", "admin", "geoserver")

# There are some configuration items that are not stored!!!

gsinsSource.writeToJson()
gsinsSource.readFromJson()
gsinsSource.putSettings()
gsinsSource.putContact()
gsinsDestination.readFromJson()
gsinsDestination.putSettings()
gsinsDestination.putContact()
