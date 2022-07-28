from api.auth.auth import *
from api.handbooks.handbooks import *
from api.images.images import *
from api.objects.objects import *

district_api = Districts()
region_api = Regions()
city_api = Cities()
city_region_api = CityRegions()
street_api = Streets()
locations_api = Locations()
handbook_api = Handbooks()
new_building_api = NewBuildings()
client_api = Clients()

catalog_api = ObjectTypes()
object_api = Objects()
apartment_api = Apartments()

object_image_api = ObjectImages()

auth_api = Auth()
user_group_api = UserGroups()
right_api = Rights()
group_api = Groups()
separation_api = Separations()
