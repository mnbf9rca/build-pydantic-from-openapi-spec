from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum

class TrainLoading(BaseModel):
    line: Optional[str] = Field(None, alias='line')
    line_direction: Optional[str] = Field(None, alias='lineDirection')
    platform_direction: Optional[str] = Field(None, alias='platformDirection')
    direction: Optional[str] = Field(None, alias='direction')
    naptan_to: Optional[str] = Field(None, alias='naptanTo')
    time_slice: Optional[str] = Field(None, alias='timeSlice')
    value: Optional[int] = Field(None, alias='value')
    model_config = {"populate_by_name": True}

class PassengerFlow(BaseModel):
    time_slice: Optional[str] = Field(None, alias='timeSlice')
    value: Optional[int] = Field(None, alias='value')
    model_config = {"populate_by_name": True}

class AdditionalProperties(BaseModel):
    category: Optional[str] = Field(None, alias='category')
    key: Optional[str] = Field(None, alias='key')
    source_system_key: Optional[str] = Field(None, alias='sourceSystemKey')
    value: Optional[str] = Field(None, alias='value')
    modified: Optional[datetime] = Field(None, alias='modified')
    model_config = {"populate_by_name": True}

class Crowding(BaseModel):
    passenger_flows: Optional[List[PassengerFlow]] = Field(None, alias='passengerFlows')
    train_loadings: Optional[List[TrainLoading]] = Field(None, alias='trainLoadings')
    model_config = {"populate_by_name": True}

class LineModeGroup(BaseModel):
    mode_name: Optional[str] = Field(None, alias='modeName')
    line_identifier: Optional[List[str]] = Field(None, alias='lineIdentifier')
    model_config = {"populate_by_name": True}

class Place(BaseModel):
    id: Optional[str] = Field(None, alias='id')
    url: Optional[str] = Field(None, alias='url')
    common_name: Optional[str] = Field(None, alias='commonName')
    distance: Optional[float] = Field(None, alias='distance')
    place_type: Optional[str] = Field(None, alias='placeType')
    additional_properties: Optional[List[AdditionalProperties]] = Field(None, alias='additionalProperties')
    children: Optional["Place"] = Field(None, alias='children')
    children_urls: Optional[List[str]] = Field(None, alias='childrenUrls')
    lat: Optional[float] = Field(None, alias='lat')
    lon: Optional[float] = Field(None, alias='lon')
    model_config = {"populate_by_name": True}

class Identifier(BaseModel):
    id: Optional[str] = Field(None, alias='id')
    name: Optional[str] = Field(None, alias='name')
    uri: Optional[str] = Field(None, alias='uri')
    full_name: Optional[str] = Field(None, alias='fullName')
    type: Optional[str] = Field(None, alias='type')
    crowding: Optional[Crowding] = Field(None, alias='crowding')
    route_type: Optional[Literal['Unknown', 'All', 'Cycle Superhighways', 'Quietways', 'Cycleways', 'Mini-Hollands', 'Central London Grid', 'Streetspace Route']] = Field(None, alias='routeType')
    status: Optional[Literal['Unknown', 'All', 'Open', 'In Progress', 'Planned', 'Planned - Subject to feasibility and consultation.', 'Not Open']] = Field(None, alias='status')
    model_config = {"populate_by_name": True}

class LineGroup(BaseModel):
    naptan_id_reference: Optional[str] = Field(None, alias='naptanIdReference')
    station_atco_code: Optional[str] = Field(None, alias='stationAtcoCode')
    line_identifier: Optional[List[str]] = Field(None, alias='lineIdentifier')
    model_config = {"populate_by_name": True}

class StopPoint(BaseModel):
    naptan_id: Optional[str] = Field(None, alias='naptanId')
    platform_name: Optional[str] = Field(None, alias='platformName')
    indicator: Optional[str] = Field(None, alias='indicator')
    stop_letter: Optional[str] = Field(None, alias='stopLetter')
    modes: Optional[List[str]] = Field(None, alias='modes')
    ics_code: Optional[str] = Field(None, alias='icsCode')
    sms_code: Optional[str] = Field(None, alias='smsCode')
    stop_type: Optional[str] = Field(None, alias='stopType')
    station_naptan: Optional[str] = Field(None, alias='stationNaptan')
    accessibility_summary: Optional[str] = Field(None, alias='accessibilitySummary')
    hub_naptan_code: Optional[str] = Field(None, alias='hubNaptanCode')
    lines: Optional[List[Identifier]] = Field(None, alias='lines')
    line_group: Optional[List[LineGroup]] = Field(None, alias='lineGroup')
    line_mode_groups: Optional[List[LineModeGroup]] = Field(None, alias='lineModeGroups')
    full_name: Optional[str] = Field(None, alias='fullName')
    naptan_mode: Optional[str] = Field(None, alias='naptanMode')
    status: Optional[bool] = Field(None, alias='status')
    id: Optional[str] = Field(None, alias='id')
    url: Optional[str] = Field(None, alias='url')
    common_name: Optional[str] = Field(None, alias='commonName')
    distance: Optional[float] = Field(None, alias='distance')
    place_type: Optional[str] = Field(None, alias='placeType')
    additional_properties: Optional[List[AdditionalProperties]] = Field(None, alias='additionalProperties')
    children: Optional[List[Place]] = Field(None, alias='children')
    children_urls: Optional[List[str]] = Field(None, alias='childrenUrls')
    lat: Optional[float] = Field(None, alias='lat')
    lon: Optional[float] = Field(None, alias='lon')
    model_config = {"populate_by_name": True}

class RouteSectionNaptanEntrySequence(BaseModel):
    ordinal: Optional[int] = Field(None, alias='ordinal')
    stop_point: Optional[StopPoint] = Field(None, alias='stopPoint')
    model_config = {"populate_by_name": True}

class TwentyFourHourClockTime(BaseModel):
    hour: Optional[str] = Field(None, alias='hour')
    minute: Optional[str] = Field(None, alias='minute')
    model_config = {"populate_by_name": True}

class ServiceFrequency(BaseModel):
    lowest_frequency: Optional[float] = Field(None, alias='lowestFrequency')
    highest_frequency: Optional[float] = Field(None, alias='highestFrequency')
    model_config = {"populate_by_name": True}

class RouteSection(BaseModel):
    id: Optional[str] = Field(None, alias='id')
    line_id: Optional[str] = Field(None, alias='lineId')
    route_code: Optional[str] = Field(None, alias='routeCode')
    name: Optional[str] = Field(None, alias='name')
    line_string: Optional[str] = Field(None, alias='lineString')
    direction: Optional[str] = Field(None, alias='direction')
    origination_name: Optional[str] = Field(None, alias='originationName')
    destination_name: Optional[str] = Field(None, alias='destinationName')
    valid_to: Optional[datetime] = Field(None, alias='validTo')
    valid_from: Optional[datetime] = Field(None, alias='validFrom')
    route_section_naptan_entry_sequence: Optional[List[RouteSectionNaptanEntrySequence]] = Field(None, alias='routeSectionNaptanEntrySequence')
    model_config = {"populate_by_name": True}

class KnownJourney(BaseModel):
    hour: Optional[str] = Field(None, alias='hour')
    minute: Optional[str] = Field(None, alias='minute')
    interval_id: Optional[int] = Field(None, alias='intervalId')
    model_config = {"populate_by_name": True}

class Period(BaseModel):
    type: Optional[Literal['Normal', 'FrequencyHours', 'FrequencyMinutes', 'Unknown']] = Field(None, alias='type')
    from_time: Optional[TwentyFourHourClockTime] = Field(None, alias='fromTime')
    to_time: Optional[TwentyFourHourClockTime] = Field(None, alias='toTime')
    frequency: Optional[ServiceFrequency] = Field(None, alias='frequency')
    model_config = {"populate_by_name": True}

class Interval(BaseModel):
    stop_id: Optional[str] = Field(None, alias='stopId')
    time_to_arrival: Optional[float] = Field(None, alias='timeToArrival')
    model_config = {"populate_by_name": True}

class Disruption(BaseModel):
    category: Optional[Literal['Undefined', 'RealTime', 'PlannedWork', 'Information', 'Event', 'Crowding', 'StatusAlert']] = Field(None, alias='category')
    type: Optional[str] = Field(None, alias='type')
    category_description: Optional[str] = Field(None, alias='categoryDescription')
    description: Optional[str] = Field(None, alias='description')
    summary: Optional[str] = Field(None, alias='summary')
    additional_info: Optional[str] = Field(None, alias='additionalInfo')
    created: Optional[datetime] = Field(None, alias='created')
    last_update: Optional[datetime] = Field(None, alias='lastUpdate')
    affected_routes: Optional[List[RouteSection]] = Field(None, alias='affectedRoutes')
    affected_stops: Optional[List[StopPoint]] = Field(None, alias='affectedStops')
    closure_text: Optional[str] = Field(None, alias='closureText')
    model_config = {"populate_by_name": True}

class ValidityPeriod(BaseModel):
    from_date: Optional[datetime] = Field(None, alias='fromDate')
    to_date: Optional[datetime] = Field(None, alias='toDate')
    is_now: Optional[bool] = Field(None, alias='isNow')
    model_config = {"populate_by_name": True}

class Schedule(BaseModel):
    name: Optional[str] = Field(None, alias='name')
    known_journeys: Optional[List[KnownJourney]] = Field(None, alias='knownJourneys')
    first_journey: Optional[KnownJourney] = Field(None, alias='firstJourney')
    last_journey: Optional[KnownJourney] = Field(None, alias='lastJourney')
    periods: Optional[List[Period]] = Field(None, alias='periods')
    model_config = {"populate_by_name": True}

class StationInterval(BaseModel):
    id: Optional[str] = Field(None, alias='id')
    intervals: Optional[List[Interval]] = Field(None, alias='intervals')
    model_config = {"populate_by_name": True}

class PredictionTiming(BaseModel):
    countdown_server_adjustment: Optional[str] = Field(None, alias='countdownServerAdjustment')
    source: Optional[datetime] = Field(None, alias='source')
    insert: Optional[datetime] = Field(None, alias='insert')
    read: Optional[datetime] = Field(None, alias='read')
    sent: Optional[datetime] = Field(None, alias='sent')
    received: Optional[datetime] = Field(None, alias='received')
    model_config = {"populate_by_name": True}

class MatchedRoute(BaseModel):
    route_code: Optional[str] = Field(None, alias='routeCode')
    name: Optional[str] = Field(None, alias='name')
    direction: Optional[str] = Field(None, alias='direction')
    origination_name: Optional[str] = Field(None, alias='originationName')
    destination_name: Optional[str] = Field(None, alias='destinationName')
    originator: Optional[str] = Field(None, alias='originator')
    destination: Optional[str] = Field(None, alias='destination')
    service_type: Optional[str] = Field(None, alias='serviceType')
    valid_to: Optional[datetime] = Field(None, alias='validTo')
    valid_from: Optional[datetime] = Field(None, alias='validFrom')
    model_config = {"populate_by_name": True}

class LineStatus(BaseModel):
    id: Optional[int] = Field(None, alias='id')
    line_id: Optional[str] = Field(None, alias='lineId')
    status_severity: Optional[int] = Field(None, alias='statusSeverity')
    status_severity_description: Optional[str] = Field(None, alias='statusSeverityDescription')
    reason: Optional[str] = Field(None, alias='reason')
    created: Optional[datetime] = Field(None, alias='created')
    modified: Optional[datetime] = Field(None, alias='modified')
    validity_periods: Optional[List[ValidityPeriod]] = Field(None, alias='validityPeriods')
    disruption: Optional[Disruption] = Field(None, alias='disruption')
    model_config = {"populate_by_name": True}

class LineServiceTypeInfo(BaseModel):
    name: Optional[str] = Field(None, alias='name')
    uri: Optional[str] = Field(None, alias='uri')
    model_config = {"populate_by_name": True}

class TimetableRoute(BaseModel):
    station_intervals: Optional[List[StationInterval]] = Field(None, alias='stationIntervals')
    schedules: Optional[List[Schedule]] = Field(None, alias='schedules')
    model_config = {"populate_by_name": True}

class DisambiguationOption(BaseModel):
    description: Optional[str] = Field(None, alias='description')
    uri: Optional[str] = Field(None, alias='uri')
    model_config = {"populate_by_name": True}

class MatchedRouteSections(BaseModel):
    id: Optional[int] = Field(None, alias='id')
    model_config = {"populate_by_name": True}

class MatchedStop(BaseModel):
    route_id: Optional[int] = Field(None, alias='routeId')
    parent_id: Optional[str] = Field(None, alias='parentId')
    station_id: Optional[str] = Field(None, alias='stationId')
    ics_id: Optional[str] = Field(None, alias='icsId')
    top_most_parent_id: Optional[str] = Field(None, alias='topMostParentId')
    direction: Optional[str] = Field(None, alias='direction')
    towards: Optional[str] = Field(None, alias='towards')
    modes: Optional[List[str]] = Field(None, alias='modes')
    stop_type: Optional[str] = Field(None, alias='stopType')
    stop_letter: Optional[str] = Field(None, alias='stopLetter')
    zone: Optional[str] = Field(None, alias='zone')
    accessibility_summary: Optional[str] = Field(None, alias='accessibilitySummary')
    has_disruption: Optional[bool] = Field(None, alias='hasDisruption')
    lines: Optional[List[Identifier]] = Field(None, alias='lines')
    status: Optional[bool] = Field(None, alias='status')
    id: Optional[str] = Field(None, alias='id')
    url: Optional[str] = Field(None, alias='url')
    name: Optional[str] = Field(None, alias='name')
    lat: Optional[float] = Field(None, alias='lat')
    lon: Optional[float] = Field(None, alias='lon')
    model_config = {"populate_by_name": True}

class LineRouteSection(BaseModel):
    route_id: Optional[int] = Field(None, alias='routeId')
    direction: Optional[str] = Field(None, alias='direction')
    destination: Optional[str] = Field(None, alias='destination')
    from_station: Optional[str] = Field(None, alias='fromStation')
    to_station: Optional[str] = Field(None, alias='toStation')
    service_type: Optional[str] = Field(None, alias='serviceType')
    vehicle_destination_text: Optional[str] = Field(None, alias='vehicleDestinationText')
    model_config = {"populate_by_name": True}

class Prediction(BaseModel):
    id: Optional[str] = Field(None, alias='id')
    operation_type: Optional[int] = Field(None, alias='operationType')
    vehicle_id: Optional[str] = Field(None, alias='vehicleId')
    naptan_id: Optional[str] = Field(None, alias='naptanId')
    station_name: Optional[str] = Field(None, alias='stationName')
    line_id: Optional[str] = Field(None, alias='lineId')
    line_name: Optional[str] = Field(None, alias='lineName')
    platform_name: Optional[str] = Field(None, alias='platformName')
    direction: Optional[str] = Field(None, alias='direction')
    bearing: Optional[str] = Field(None, alias='bearing')
    destination_naptan_id: Optional[str] = Field(None, alias='destinationNaptanId')
    destination_name: Optional[str] = Field(None, alias='destinationName')
    timestamp: Optional[datetime] = Field(None, alias='timestamp')
    time_to_station: Optional[int] = Field(None, alias='timeToStation')
    current_location: Optional[str] = Field(None, alias='currentLocation')
    towards: Optional[str] = Field(None, alias='towards')
    expected_arrival: Optional[datetime] = Field(None, alias='expectedArrival')
    time_to_live: Optional[datetime] = Field(None, alias='timeToLive')
    mode_name: Optional[str] = Field(None, alias='modeName')
    timing: Optional[PredictionTiming] = Field(None, alias='timing')
    model_config = {"populate_by_name": True}

class ActiveServiceType(BaseModel):
    mode: Optional[str] = Field(None, alias='mode')
    service_type: Optional[str] = Field(None, alias='serviceType')
    model_config = {"populate_by_name": True}

class Line(BaseModel):
    id: Optional[str] = Field(None, alias='id')
    name: Optional[str] = Field(None, alias='name')
    mode_name: Optional[str] = Field(None, alias='modeName')
    disruptions: Optional[List[Disruption]] = Field(None, alias='disruptions')
    created: Optional[datetime] = Field(None, alias='created')
    modified: Optional[datetime] = Field(None, alias='modified')
    line_statuses: Optional[List[LineStatus]] = Field(None, alias='lineStatuses')
    route_sections: Optional[List[MatchedRoute]] = Field(None, alias='routeSections')
    service_types: Optional[List[LineServiceTypeInfo]] = Field(None, alias='serviceTypes')
    crowding: Optional[Crowding] = Field(None, alias='crowding')
    model_config = {"populate_by_name": True}

class StatusSeverity(BaseModel):
    mode_name: Optional[str] = Field(None, alias='modeName')
    severity_level: Optional[int] = Field(None, alias='severityLevel')
    description: Optional[str] = Field(None, alias='description')
    model_config = {"populate_by_name": True}

class Mode(BaseModel):
    is_tfl_service: Optional[bool] = Field(None, alias='isTflService')
    is_fare_paying: Optional[bool] = Field(None, alias='isFarePaying')
    is_scheduled_service: Optional[bool] = Field(None, alias='isScheduledService')
    mode_name: Optional[str] = Field(None, alias='modeName')
    model_config = {"populate_by_name": True}

class SearchMatch(BaseModel):
    id: Optional[str] = Field(None, alias='id')
    url: Optional[str] = Field(None, alias='url')
    name: Optional[str] = Field(None, alias='name')
    lat: Optional[float] = Field(None, alias='lat')
    lon: Optional[float] = Field(None, alias='lon')
    model_config = {"populate_by_name": True}

class LineSpecificServiceType(BaseModel):
    service_type: Optional[LineServiceTypeInfo] = Field(None, alias='serviceType')
    stop_serves_service_type: Optional[bool] = Field(None, alias='stopServesServiceType')
    model_config = {"populate_by_name": True}

class Timetable(BaseModel):
    departure_stop_id: Optional[str] = Field(None, alias='departureStopId')
    routes: Optional[List[TimetableRoute]] = Field(None, alias='routes')
    model_config = {"populate_by_name": True}

class Disambiguation(BaseModel):
    disambiguation_options: Optional[List[DisambiguationOption]] = Field(None, alias='disambiguationOptions')
    model_config = {"populate_by_name": True}

class RouteSearchMatch(BaseModel):
    line_id: Optional[str] = Field(None, alias='lineId')
    mode: Optional[str] = Field(None, alias='mode')
    line_name: Optional[str] = Field(None, alias='lineName')
    line_route_section: Optional[List[LineRouteSection]] = Field(None, alias='lineRouteSection')
    matched_route_sections: Optional[List[MatchedRouteSections]] = Field(None, alias='matchedRouteSections')
    matched_stops: Optional[List[MatchedStop]] = Field(None, alias='matchedStops')
    id: Optional[str] = Field(None, alias='id')
    url: Optional[str] = Field(None, alias='url')
    name: Optional[str] = Field(None, alias='name')
    lat: Optional[float] = Field(None, alias='lat')
    lon: Optional[float] = Field(None, alias='lon')
    model_config = {"populate_by_name": True}

class OrderedRoute(BaseModel):
    name: Optional[str] = Field(None, alias='name')
    naptan_ids: Optional[List[str]] = Field(None, alias='naptanIds')
    service_type: Optional[str] = Field(None, alias='serviceType')
    model_config = {"populate_by_name": True}

class StopPointSequence(BaseModel):
    line_id: Optional[str] = Field(None, alias='lineId')
    line_name: Optional[str] = Field(None, alias='lineName')
    direction: Optional[str] = Field(None, alias='direction')
    branch_id: Optional[int] = Field(None, alias='branchId')
    next_branch_ids: Optional[List[int]] = Field(None, alias='nextBranchIds')
    prev_branch_ids: Optional[List[int]] = Field(None, alias='prevBranchIds')
    stop_point: Optional[List[MatchedStop]] = Field(None, alias='stopPoint')
    service_type: Optional[Literal['Regular', 'Night']] = Field(None, alias='serviceType')
    model_config = {"populate_by_name": True}

ArrayOfPrediction = List[Prediction]

ArrayOfActiveServiceType = List[ActiveServiceType]

ArrayOfDisruption = List[Disruption]

ArrayOfStopPoint = List[StopPoint]

ArrayOfLine = List[Line]

ArrayOfStatusSeverity = List[StatusSeverity]

ArrayOfMode = List[Mode]

class SearchResponse(BaseModel):
    query: Optional[str] = Field(None, alias='query')
    from_field: Optional[int] = Field(None, alias='from')
    page: Optional[int] = Field(None, alias='page')
    page_size: Optional[int] = Field(None, alias='pageSize')
    provider: Optional[str] = Field(None, alias='provider')
    total: Optional[int] = Field(None, alias='total')
    matches: Optional[List[SearchMatch]] = Field(None, alias='matches')
    max_score: Optional[float] = Field(None, alias='maxScore')
    model_config = {"populate_by_name": True}

class StopPointsResponse(BaseModel):
    centre_point: Optional[List[float]] = Field(None, alias='centrePoint')
    stop_points: Optional[List[StopPoint]] = Field(None, alias='stopPoints')
    page_size: Optional[int] = Field(None, alias='pageSize')
    total: Optional[int] = Field(None, alias='total')
    page: Optional[int] = Field(None, alias='page')
    model_config = {"populate_by_name": True}

class DisruptedPoint(BaseModel):
    atco_code: Optional[str] = Field(None, alias='atcoCode')
    from_date: Optional[datetime] = Field(None, alias='fromDate')
    to_date: Optional[datetime] = Field(None, alias='toDate')
    description: Optional[str] = Field(None, alias='description')
    common_name: Optional[str] = Field(None, alias='commonName')
    type: Optional[str] = Field(None, alias='type')
    mode: Optional[str] = Field(None, alias='mode')
    station_atco_code: Optional[str] = Field(None, alias='stationAtcoCode')
    appearance: Optional[str] = Field(None, alias='appearance')
    additional_information: Optional[str] = Field(None, alias='additionalInformation')
    model_config = {"populate_by_name": True}

class StopPointRouteSection(BaseModel):
    naptan_id: Optional[str] = Field(None, alias='naptanId')
    line_id: Optional[str] = Field(None, alias='lineId')
    mode: Optional[str] = Field(None, alias='mode')
    valid_from: Optional[datetime] = Field(None, alias='validFrom')
    valid_to: Optional[datetime] = Field(None, alias='validTo')
    direction: Optional[str] = Field(None, alias='direction')
    route_section_name: Optional[str] = Field(None, alias='routeSectionName')
    line_string: Optional[str] = Field(None, alias='lineString')
    is_active: Optional[bool] = Field(None, alias='isActive')
    service_type: Optional[str] = Field(None, alias='serviceType')
    vehicle_destination_text: Optional[str] = Field(None, alias='vehicleDestinationText')
    destination_name: Optional[str] = Field(None, alias='destinationName')
    model_config = {"populate_by_name": True}

class ArrivalDeparture(BaseModel):
    platform_name: Optional[str] = Field(None, alias='platformName')
    destination_naptan_id: Optional[str] = Field(None, alias='destinationNaptanId')
    destination_name: Optional[str] = Field(None, alias='destinationName')
    naptan_id: Optional[str] = Field(None, alias='naptanId')
    station_name: Optional[str] = Field(None, alias='stationName')
    estimated_time_of_arrival: Optional[datetime] = Field(None, alias='estimatedTimeOfArrival')
    scheduled_time_of_arrival: Optional[datetime] = Field(None, alias='scheduledTimeOfArrival')
    estimated_time_of_departure: Optional[datetime] = Field(None, alias='estimatedTimeOfDeparture')
    scheduled_time_of_departure: Optional[datetime] = Field(None, alias='scheduledTimeOfDeparture')
    minutes_and_seconds_to_arrival: Optional[str] = Field(None, alias='minutesAndSecondsToArrival')
    minutes_and_seconds_to_departure: Optional[str] = Field(None, alias='minutesAndSecondsToDeparture')
    cause: Optional[str] = Field(None, alias='cause')
    departure_status: Optional[Literal['OnTime', 'Delayed', 'Cancelled', 'NotStoppingAtStation']] = Field(None, alias='departureStatus')
    timing: Optional[PredictionTiming] = Field(None, alias='timing')
    model_config = {"populate_by_name": True}

class LineServiceType(BaseModel):
    line_name: Optional[str] = Field(None, alias='lineName')
    line_specific_service_types: Optional[List[LineSpecificServiceType]] = Field(None, alias='lineSpecificServiceTypes')
    model_config = {"populate_by_name": True}

class StopPointCategory(BaseModel):
    category: Optional[str] = Field(None, alias='category')
    available_keys: Optional[List[str]] = Field(None, alias='availableKeys')
    model_config = {"populate_by_name": True}

class TimetableResponse(BaseModel):
    line_id: Optional[str] = Field(None, alias='lineId')
    line_name: Optional[str] = Field(None, alias='lineName')
    direction: Optional[str] = Field(None, alias='direction')
    pdf_url: Optional[str] = Field(None, alias='pdfUrl')
    stations: Optional[List[MatchedStop]] = Field(None, alias='stations')
    stops: Optional[List[MatchedStop]] = Field(None, alias='stops')
    timetable: Optional[Timetable] = Field(None, alias='timetable')
    disambiguation: Optional[Disambiguation] = Field(None, alias='disambiguation')
    status_error_message: Optional[str] = Field(None, alias='statusErrorMessage')
    model_config = {"populate_by_name": True}

class RouteSearchResponse(BaseModel):
    input: Optional[str] = Field(None, alias='input')
    search_matches: Optional[List[RouteSearchMatch]] = Field(None, alias='searchMatches')
    model_config = {"populate_by_name": True}

class RouteSequence(BaseModel):
    line_id: Optional[str] = Field(None, alias='lineId')
    line_name: Optional[str] = Field(None, alias='lineName')
    direction: Optional[str] = Field(None, alias='direction')
    is_outbound_only: Optional[bool] = Field(None, alias='isOutboundOnly')
    mode: Optional[str] = Field(None, alias='mode')
    line_strings: Optional[List[str]] = Field(None, alias='lineStrings')
    stations: Optional[List[MatchedStop]] = Field(None, alias='stations')
    stop_point_sequences: Optional[List[StopPointSequence]] = Field(None, alias='stopPointSequences')
    ordered_line_routes: Optional[List[OrderedRoute]] = Field(None, alias='orderedLineRoutes')
    model_config = {"populate_by_name": True}

Place.model_rebuild()
