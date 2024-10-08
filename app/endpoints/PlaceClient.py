from ..Client import Client
from .PlaceClient_config import endpoints
from .. import models
from ..package_models import ApiError

class PlaceClient(Client):
    def metacategories(self, ) -> models.PlaceCategoryArray | ApiError:
        '''
        Gets a list of all of the available place property categories and keys.

        Parameters:
        No parameters required.
        '''
        return self._send_request_and_deserialize(endpoints['Place_MetaCategories'], endpoint_args=None)

    def metaplacetypes(self, ) -> models.PlaceCategoryArray | ApiError:
        '''
        Gets a list of the available types of Place.

        Parameters:
        No parameters required.
        '''
        return self._send_request_and_deserialize(endpoints['Place_MetaPlaceTypes'], endpoint_args=None)

    def getbytypebypathtypesqueryactiveonly(self, types: str, activeOnly: bool | None = None) -> models.PlaceArray | ApiError:
        '''
        Gets all places of a given type

        Parameters:
        types: str - A comma-separated list of the types to return. Max. approx 12 types.
            A valid list of place types can be obtained from the /Place/Meta/placeTypes endpoint.. Example: CarPark
        activeOnly: bool - An optional parameter to limit the results to active records only (Currently only the 'VariableMessageSign' place type is supported). Example: None given
        '''
        return self._send_request_and_deserialize(endpoints['Place_GetByTypeByPathTypesQueryActiveOnly'], params=[types], endpoint_args={ 'activeOnly': activeOnly })

    def getbypathidqueryincludechildren(self, id: str, includeChildren: bool | None = None) -> models.PlaceArray | ApiError:
        '''
        Gets the place with the given id.

        Parameters:
        id: str - The id of the place, you can use the /Place/Types/{types} endpoint to get a list of places for a given type including their ids. Example: CarParks_800491
        includeChildren: bool - Defaults to false. If true child places e.g. individual charging stations at a charge point while be included, otherwise just the URLs of any child places will be returned. Example: None given
        '''
        return self._send_request_and_deserialize(endpoints['Place_GetByPathIdQueryIncludeChildren'], params=[id], endpoint_args={ 'includeChildren': includeChildren })

    def getbygeopointbyquerylatquerylonqueryradiusquerycategoriesqueryincludec(self, Lat: float, Lon: float, radius: float | None = None, categories: list | None = None, includeChildren: bool | None = None, type: list | None = None, activeOnly: bool | None = None, numberOfPlacesToReturn: int | None = None) -> models.StopPointArray | ApiError:
        '''
        Gets the places that lie within a geographic region. The geographic region of interest can either be specified by using a lat/lon geo-point and a radius in metres to return places within the locus defined by the lat/lon of its centre or alternatively, by the use of a bounding box defined by the lat/lon of its north-west and south-east corners. Optionally filters on type and can strip properties for a smaller payload.

        Parameters:
        Lat: float - Format - double. lat is latitude of the centre of the bounding circle.. Example: 51.5029703
        Lon: float - Format - double. lon is longitude of the centre of the bounding circle.. Example: -0.1365283
        radius: float - Format - double. The radius of the bounding circle in metres when only lat/lon are specified.. Example: 100
        categories: list - An optional list of comma separated property categories to return in the Place's property bag. If null or empty, all categories of property are returned. Pass the keyword "none" to return no properties (a valid list of categories can be obtained from the /Place/Meta/categories endpoint). Example: None given
        includeChildren: bool - Defaults to false. If true child places e.g. individual charging stations at a charge point while be included, otherwise just the URLs of any child places will be returned. Example: None given
        type: list - Place types to filter on, or null to return all types. Example: None given
        activeOnly: bool - An optional parameter to limit the results to active records only (Currently only the 'VariableMessageSign' place type is supported). Example: None given
        numberOfPlacesToReturn: int - Format - int32. If specified, limits the number of returned places equal to the given value. Example: None given
        '''
        return self._send_request_and_deserialize(endpoints['Place_GetByGeoPointByQueryLatQueryLonQueryRadiusQueryCategoriesQueryIncludeC'], endpoint_args={ 'Lat': Lat, 'Lon': Lon, 'radius': radius, 'categories': categories, 'includeChildren': includeChildren, 'type': type, 'activeOnly': activeOnly, 'numberOfPlacesToReturn': numberOfPlacesToReturn })

    def getatbypathtypepathlatpathlon(self, type: str, lat: float, lon: float) -> models.Object | ApiError:
        '''
        Gets any places of the given type whose geography intersects the given latitude and longitude. In practice this means the Place must be polygonal e.g. a BoroughBoundary.

        Parameters:
        type: str - The place type (a valid list of place types can be obtained from the /Place/Meta/placeTypes endpoint). Example: CarPark
        lat: float - Format - double. lat is latitude of the centre of the bounding circle.. Example: 51.5029703
        lon: float - Format - double. lon is longitude of the centre of the bounding circle. Example: -0.1365283
        '''
        return self._send_request_and_deserialize(endpoints['Place_GetAtByPathTypePathLatPathLon'], params=[type, lat, lon], endpoint_args=None)

    def searchbyquerynamequerytypes(self, name: str, types: list | None = None) -> models.PlaceArray | ApiError:
        '''
        Gets all places that matches the given query

        Parameters:
        name: str - The name of the place, you can use the /Place/Types/{types} endpoint to get a list of places for a given type including their names.. Example: Bridge
        types: list - A comma-separated list of the types to return. Max. approx 12 types.. Example: None given
        '''
        return self._send_request_and_deserialize(endpoints['Place_SearchByQueryNameQueryTypes'], endpoint_args={ 'name': name, 'types': types })

    def proxy(self, ) -> models.ObjectResponse | ApiError:
        '''
        Forwards any remaining requests to the back-end

        Parameters:
        No parameters required.
        '''
        return self._send_request_and_deserialize(endpoints['Forward_Proxy'], endpoint_args=None)

