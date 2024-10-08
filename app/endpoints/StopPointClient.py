from ..Client import Client
from .StopPointClient_config import endpoints
from .. import models
from ..package_models import ApiError

class StopPointClient(Client):
    def metacategories(self, ) -> models.PlaceCategoryArray | ApiError:
        '''
        Gets the list of available StopPoint additional information categories

        Parameters:
        No parameters required.
        '''
        return self._send_request_and_deserialize(endpoints['StopPoint_MetaCategories'], endpoint_args=None)

    def proxy(self, ) -> models.GenericResponseModel | ApiError:
        '''
        Forwards any remaining requests to the back-end

        Parameters:
        No parameters required.
        '''
        return self._send_request_and_deserialize(endpoints['Forward_Proxy'], endpoint_args=None)

    def metastoptypes(self, ) -> models.GenericResponseModel | ApiError:
        '''
        Gets the list of available StopPoint types

        Parameters:
        No parameters required.
        '''
        return self._send_request_and_deserialize(endpoints['StopPoint_MetaStopTypes'], endpoint_args=None)

    def metamodes(self, ) -> models.ModeArray | ApiError:
        '''
        Gets the list of available StopPoint modes

        Parameters:
        No parameters required.
        '''
        return self._send_request_and_deserialize(endpoints['StopPoint_MetaModes'], endpoint_args=None)

    def getbypathidsqueryincludecrowdingdata(self, ids: str, includeCrowdingData: bool | None = None) -> models.StopPointArray | ApiError:
        '''
        Gets a list of StopPoints corresponding to the given list of stop ids.

        Parameters:
        ids: str - A comma-separated list of stop point ids (station naptan code e.g. 940GZZLUASL). Max. approx. 20 ids.
            You can use /StopPoint/Search/{query} endpoint to find a stop point id from a station name.. Example: HUBWAT
        includeCrowdingData: bool - Include the crowding data (static). To Filter further use: /StopPoint/{ids}/Crowding/{line}. Example: None given
        '''
        return self._send_request_and_deserialize(endpoints['StopPoint_GetByPathIdsQueryIncludeCrowdingData'], params=[ids], endpoint_args={ 'includeCrowdingData': includeCrowdingData })

    def getbypathidqueryplacetypes(self, id: str, placeTypes: str) -> models.PlaceArray | ApiError:
        '''
        Get a list of places corresponding to a given id and place types.

        Parameters:
        id: str - A naptan id for a stop point (station naptan code e.g. 940GZZLUASL).. Example: 930GWMP
        placeTypes: str - A comcomma-separated value representing the place types.. Example: NaptanFerryEntrance
        '''
        return self._send_request_and_deserialize(endpoints['StopPoint_GetByPathIdQueryPlaceTypes'], params=[id], endpoint_args={ 'placeTypes': placeTypes })

    def crowdingbypathidpathlinequerydirection(self, id: str, line: str, direction: str) -> models.StopPointArray | ApiError:
        '''
        Gets all the Crowding data (static) for the StopPointId, plus crowding data for a given line and optionally a particular direction.

        Parameters:
        id: str - The Naptan id of the stop. Example: 940GZZLUSWK
        line: str - A particular line e.g. victoria, circle, northern etc.. Example: jubilee
        direction: str - The direction of travel. Can be inbound or outbound.. Example: all
        '''
        return self._send_request_and_deserialize(endpoints['StopPoint_CrowdingByPathIdPathLineQueryDirection'], params=[id, line], endpoint_args={ 'direction': direction })

    def getbytypebypathtypes(self, types: str) -> models.StopPointArray | ApiError:
        '''
        Gets all stop points of a given type

        Parameters:
        types: str - A comma-separated list of the types to return. Max. approx. 12 types. 
            A list of valid stop types can be obtained from the StopPoint/meta/stoptypes endpoint.. Example: TransportInterchange
        '''
        return self._send_request_and_deserialize(endpoints['StopPoint_GetByTypeByPathTypes'], params=[types], endpoint_args=None)

    def getbytypewithpaginationbypathtypespathpage(self, types: str, page: int) -> models.StopPointArray | ApiError:
        '''
        Gets all the stop points of given type(s) with a page number

        Parameters:
        types: str - . Example: TransportInterchange
        page: int - Format - int32.. Example: 1
        '''
        return self._send_request_and_deserialize(endpoints['StopPoint_GetByTypeWithPaginationByPathTypesPathPage'], params=[types, page], endpoint_args=None)

    def getservicetypesbyqueryidquerylineidsquerymodes(self, id: str, lineIds: list | None = None, modes: list | None = None) -> models.LineServiceTypeArray | ApiError:
        '''
        Gets the service types for a given stoppoint

        Parameters:
        id: str - The Naptan id of the stop. Example: 910GSTJMSST
        lineIds: list - The lines which contain the given Naptan id (all lines relevant to the given stoppoint if empty). Example: None given
        modes: list - The modes which the lines are relevant to (all if empty). Example: None given
        '''
        return self._send_request_and_deserialize(endpoints['StopPoint_GetServiceTypesByQueryIdQueryLineIdsQueryModes'], endpoint_args={ 'id': id, 'lineIds': lineIds, 'modes': modes })

    def arrivalsbypathid(self, id: str) -> models.PredictionArray | ApiError:
        '''
        Gets the list of arrival predictions for the given stop point id

        Parameters:
        id: str - A StopPoint id (station naptan code e.g. 940GZZLUASL, you can use /StopPoint/Search/{query} endpoint to find a stop point id from a station name). Example: HUBWAT
        '''
        return self._send_request_and_deserialize(endpoints['StopPoint_ArrivalsByPathId'], params=[id], endpoint_args=None)

    def arrivaldeparturesbypathidquerylineids(self, id: str, lineIds: str) -> models.ArrivalDepartureArray | ApiError:
        '''
        Gets the list of arrival and departure predictions for the given stop point id (overground and tfl rail only)

        Parameters:
        id: str - A StopPoint id (station naptan code e.g. 940GZZLUASL, you can use /StopPoint/Search/{query} endpoint to find a stop point id from a station name). Example: 910GLIVST
        lineIds: str - A comma-separated list of line ids e.g. tfl-rail, london-overground. Example: elizabeth
        '''
        return self._send_request_and_deserialize(endpoints['StopPoint_ArrivalDeparturesByPathIdQueryLineIds'], params=[id], endpoint_args={ 'lineIds': lineIds })

    def reachablefrombypathidpathlineidqueryservicetypes(self, id: str, lineId: str, serviceTypes: str | None = None) -> models.StopPointArray | ApiError:
        '''
        Gets Stopoints that are reachable from a station/line combination.

        Parameters:
        id: str - The id (station naptan code e.g. 940GZZLUASL, you can use /StopPoint/Search/{query} endpoint to find a stop point id from a station name) of the stop point to filter by. Example: 940GZZLUASL
        lineId: str - Line id of the line to filter by (e.g. victoria). Example: Piccadilly
        serviceTypes: str - A comma-separated list of service types to filter on. If not specified. Supported values: Regular, Night. Defaulted to 'Regular' if not specified. Example: Regular
        '''
        return self._send_request_and_deserialize(endpoints['StopPoint_ReachableFromByPathIdPathLineIdQueryServiceTypes'], params=[id, lineId], endpoint_args={ 'serviceTypes': serviceTypes })

    def routebypathidqueryservicetypes(self, id: str, serviceTypes: str | None = None) -> models.StopPointRouteSectionArray | ApiError:
        '''
        Returns the route sections for all the lines that service the given stop point ids

        Parameters:
        id: str - A stop point id (station naptan codes e.g. 940GZZLUASL, you can use /StopPoint/Search/{query} endpoint to find a stop point id from a station name). Example: 940GZZLUASL
        serviceTypes: str - A comma-separated list of service types to filter on. If not specified. Supported values: Regular, Night. Defaulted to 'Regular' if not specified. Example: Regular
        '''
        return self._send_request_and_deserialize(endpoints['StopPoint_RouteByPathIdQueryServiceTypes'], params=[id], endpoint_args={ 'serviceTypes': serviceTypes })

    def disruptionbymodebypathmodesqueryincluderouteblockedstops(self, modes: str, includeRouteBlockedStops: bool | None = None) -> models.DisruptedPointArray | ApiError:
        '''
        Gets a distinct list of disrupted stop points for the given modes

        Parameters:
        modes: str - A comma-seperated list of modes e.g. tube,dlr. Example: Tube
        includeRouteBlockedStops: bool - . Example: None given
        '''
        return self._send_request_and_deserialize(endpoints['StopPoint_DisruptionByModeByPathModesQueryIncludeRouteBlockedStops'], params=[modes], endpoint_args={ 'includeRouteBlockedStops': includeRouteBlockedStops })

    def disruptionbypathidsquerygetfamilyqueryincluderouteblockedstopsquer(self, ids: str, getFamily: bool | None = None, includeRouteBlockedStops: bool | None = None, flattenResponse: bool | None = None) -> models.DisruptedPointArray | ApiError:
        '''
        Gets all disruptions for the specified StopPointId, plus disruptions for any child Naptan records it may have.

        Parameters:
        ids: str - A comma-seperated list of stop point ids. Max. approx. 20 ids.
            You can use /StopPoint/Search/{query} endpoint to find a stop point id from a station name.. Example: 940GZZLUASL
        getFamily: bool - Specify true to return disruptions for entire family, or false to return disruptions for just this stop point. Defaults to false.. Example: None given
        includeRouteBlockedStops: bool - . Example: None given
        flattenResponse: bool - Specify true to associate all disruptions with parent stop point. (Only applicable when getFamily is true).. Example: None given
        '''
        return self._send_request_and_deserialize(endpoints['StopPoint_DisruptionByPathIdsQueryGetFamilyQueryIncludeRouteBlockedStopsQuer'], params=[ids], endpoint_args={ 'getFamily': getFamily, 'includeRouteBlockedStops': includeRouteBlockedStops, 'flattenResponse': flattenResponse })

    def directionbypathidpathtostoppointidquerylineid(self, id: str, toStopPointId: str, lineId: str | None = None) -> models.GenericResponseModel | ApiError:
        '''
        Returns the canonical direction, "inbound" or "outbound", for a given pair of stop point Ids in the direction from -&gt; to.

        Parameters:
        id: str - Originating stop id (station naptan code e.g. 940GZZLUASL, you can use /StopPoint/Search/{query} endpoint to find a stop point id from a station name). Example: 940GZZLUASL
        toStopPointId: str - Destination stop id (station naptan code e.g. 940GZZLUASL, you can use /StopPoint/Search/{query} endpoint to find a stop point id from a station name). Example: 940GZZLUHWY
        lineId: str - Optional line id filter e.g. victoria. Example: None given
        '''
        return self._send_request_and_deserialize(endpoints['StopPoint_DirectionByPathIdPathToStopPointIdQueryLineId'], params=[id, toStopPointId], endpoint_args={ 'lineId': lineId })

    def getbygeopointbyquerylatquerylonquerystoptypesqueryradiusqueryusest(self, lat: float, lon: float, stopTypes: str, radius: int | None = None, useStopPointHierarchy: bool | None = None, modes: list | None = None, categories: list | None = None, returnLines: bool | None = None) -> models.StopPointsResponse | ApiError:
        '''
        Gets a list of StopPoints within {radius} by the specified criteria

        Parameters:
        lat: float - Format - double. the latitude of the centre of the bounding circle. Example: 51.5
        lon: float - Format - double. the longitude of the centre of the bounding circle. Example: 0.12
        stopTypes: str - a list of stopTypes that should be returned (a list of valid stop types can be obtained from the StopPoint/meta/stoptypes endpoint). Example: NaptanCoachBay
        radius: int - Format - int32. the radius of the bounding circle in metres (default : 200). Example: None given
        useStopPointHierarchy: bool - Re-arrange the output into a parent/child hierarchy. Example: None given
        modes: list - the list of modes to search (comma separated mode names e.g. tube,dlr). Example: None given
        categories: list - an optional list of comma separated property categories to return in the StopPoint's property bag. If null or empty, all categories of property are returned. Pass the keyword "none" to return no properties (a valid list of categories can be obtained from the /StopPoint/Meta/categories endpoint). Example: None given
        returnLines: bool - true to return the lines that each stop point serves as a nested resource. Example: None given
        '''
        return self._send_request_and_deserialize(endpoints['StopPoint_GetByGeoPointByQueryLatQueryLonQueryStopTypesQueryRadiusQueryUseSt'], endpoint_args={ 'lat': lat, 'lon': lon, 'stopTypes': stopTypes, 'radius': radius, 'useStopPointHierarchy': useStopPointHierarchy, 'modes': modes, 'categories': categories, 'returnLines': returnLines })

    def getbymodebypathmodesquerypage(self, modes: str, page: int | None = None) -> models.StopPointsResponse | ApiError:
        '''
        Gets a list of StopPoints filtered by the modes available at that StopPoint.

        Parameters:
        modes: str - A comma-seperated list of modes e.g. tube,dlr. Example: Tube
        page: int - Format - int32. The data set page to return. Page 1 equates to the first 1000 stop points, page 2 equates to 1001-2000 etc. Must be entered for bus mode as data set is too large.. Example: None given
        '''
        return self._send_request_and_deserialize(endpoints['StopPoint_GetByModeByPathModesQueryPage'], params=[modes], endpoint_args={ 'page': page })

    def searchbypathqueryquerymodesqueryfaresonlyquerymaxresultsquerylines(self, query: str, modes: list | None = None, faresOnly: bool | None = None, maxResults: int | None = None, lines: list | None = None, includeHubs: bool | None = None, tflOperatedNationalRailStationsOnly: bool | None = None) -> models.SearchResponse | ApiError:
        '''
        Search StopPoints by their common name, or their 5-digit Countdown Bus Stop Code.

        Parameters:
        query: str - The query string, case-insensitive. Leading and trailing wildcards are applied automatically.. Example: Waterloo
        modes: list - An optional, parameter separated list of the modes to filter by. Example: None given
        faresOnly: bool - True to only return stations in that have Fares data available for single fares to another station.. Example: None given
        maxResults: int - Format - int32. An optional result limit, defaulting to and with a maximum of 50. Since children of the stop point heirarchy are returned for matches,
            it is possible that the flattened result set will contain more than 50 items.. Example: None given
        lines: list - An optional, parameter separated list of the lines to filter by. Example: None given
        includeHubs: bool - If true, returns results including HUBs.. Example: None given
        tflOperatedNationalRailStationsOnly: bool - If the national-rail mode is included, this flag will filter the national rail stations so that only those operated by TfL are returned. Example: None given
        '''
        return self._send_request_and_deserialize(endpoints['StopPoint_SearchByPathQueryQueryModesQueryFaresOnlyQueryMaxResultsQueryLines'], params=[query], endpoint_args={ 'modes': modes, 'faresOnly': faresOnly, 'maxResults': maxResults, 'lines': lines, 'includeHubs': includeHubs, 'tflOperatedNationalRailStationsOnly': tflOperatedNationalRailStationsOnly })

    def searchbyqueryqueryquerymodesqueryfaresonlyquerymaxresultsqueryline(self, query: str, modes: list | None = None, faresOnly: bool | None = None, maxResults: int | None = None, lines: list | None = None, includeHubs: bool | None = None, tflOperatedNationalRailStationsOnly: bool | None = None) -> models.SearchResponse | ApiError:
        '''
        Search StopPoints by their common name, or their 5-digit Countdown Bus Stop Code.

        Parameters:
        query: str - The query string, case-insensitive. Leading and trailing wildcards are applied automatically.. Example: Waterloo
        modes: list - An optional, parameter separated list of the modes to filter by. Example: None given
        faresOnly: bool - True to only return stations in that have Fares data available for single fares to another station.. Example: None given
        maxResults: int - Format - int32. An optional result limit, defaulting to and with a maximum of 50. Since children of the stop point heirarchy are returned for matches,
            it is possible that the flattened result set will contain more than 50 items.. Example: None given
        lines: list - An optional, parameter separated list of the lines to filter by. Example: None given
        includeHubs: bool - If true, returns results including HUBs.. Example: None given
        tflOperatedNationalRailStationsOnly: bool - If the national-rail mode is included, this flag will filter the national rail stations so that only those operated by TfL are returned. Example: None given
        '''
        return self._send_request_and_deserialize(endpoints['StopPoint_SearchByQueryQueryQueryModesQueryFaresOnlyQueryMaxResultsQueryLine'], endpoint_args={ 'query': query, 'modes': modes, 'faresOnly': faresOnly, 'maxResults': maxResults, 'lines': lines, 'includeHubs': includeHubs, 'tflOperatedNationalRailStationsOnly': tflOperatedNationalRailStationsOnly })

    def getbysmsbypathidqueryoutput(self, id: str, output: str | None = None) -> models.Object | ApiError:
        '''
        Gets a StopPoint for a given sms code.

        Parameters:
        id: str - A 5-digit Countdown Bus Stop Code e.g. 73241, 50435, 56334.. Example: 73241
        output: str - If set to "web", a 302 redirect to relevant website bus stop page is returned. Valid values are : web. All other values are ignored.. Example: None given
        '''
        return self._send_request_and_deserialize(endpoints['StopPoint_GetBySmsByPathIdQueryOutput'], params=[id], endpoint_args={ 'output': output })

    def gettaxiranksbyidsbypathstoppointid(self, stopPointId: str) -> models.PlaceArray | ApiError:
        '''
        Gets a list of taxi ranks corresponding to the given stop point id.

        Parameters:
        stopPointId: str - stopPointId is required to get the taxi ranks.. Example: HUBWAT
        '''
        return self._send_request_and_deserialize(endpoints['StopPoint_GetTaxiRanksByIdsByPathStopPointId'], params=[stopPointId], endpoint_args=None)

    def getcarparksbyidbypathstoppointid(self, stopPointId: str) -> models.PlaceArray | ApiError:
        '''
        Get car parks corresponding to the given stop point id.

        Parameters:
        stopPointId: str - stopPointId is required to get the car parks.. Example: HUBWAT
        '''
        return self._send_request_and_deserialize(endpoints['StopPoint_GetCarParksByIdByPathStopPointId'], params=[stopPointId], endpoint_args=None)

