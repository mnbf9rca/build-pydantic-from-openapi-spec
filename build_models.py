import json
import os
import logging
import re
import keyword
from enum import Enum
from typing import Dict, Any, Optional, Union, Type, List, Set, get_origin, get_args, Literal, ForwardRef, Tuple
from pydantic import BaseModel, create_model, Field
from datetime import datetime
from collections import defaultdict, deque

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# mappings from https://techforum.tfl.gov.uk/t/swagger-file-outdated/2085/8
# slightly modified to be a dictionary of dictionaries with no arrays
# previously PlaceCategory and StopPointCategory were both listed for each (as an array)
# the TfL api does seem to differentiate them now
tfl_mappings = {
    "AccidentStats": {
        "Tfl-Api-Presentation-Entities-AccidentStats-AccidentDetailArray": "Tfl-Api-Presentation-Entities-AccidentStats-AccidentDetailArray",
        "Tfl-Api-Presentation-Entities-AccidentStats-AccidentDetailArray-1": "Tfl-Api-Presentation-Entities-AccidentStats-AccidentDetailArray-1",
        "Tfl-Api-Presentation-Entities-AccidentStats-AccidentDetailArray-2": "Tfl-Api-Presentation-Entities-AccidentStats-AccidentDetailArray-2",
        "Tfl-Api-Presentation-Entities-AccidentStats-AccidentDetailArray-3": "Tfl-Api-Presentation-Entities-AccidentStats-AccidentDetailArray-3",
        "Tfl.Api.Presentation.Entities.AccidentStats.AccidentDetail": "Tfl.Api.Presentation.Entities.AccidentStats.AccidentDetail",
        "Tfl.Api.Presentation.Entities.AccidentStats.Casualty": "Tfl.Api.Presentation.Entities.AccidentStats.Casualty",
        "Tfl.Api.Presentation.Entities.AccidentStats.Vehicle": "Tfl.Api.Presentation.Entities.AccidentStats.Vehicle",
    },
    "AirQuality": {"System.Object": "Tfl.Api.Presentation.Entities.LondonAirForecast"},
    "BikePoint": {
        "Tfl-Api-Presentation-Entities-PlaceArray": "PlaceArray",
        "Tfl.Api.Presentation.Entities.Place": "Tfl.Api.Presentation.Entities.Place",
        "Tfl.Api.Presentation.Entities.AdditionalProperties": "Tfl.Api.Presentation.Entities.AdditionalProperties",
        "Tfl-Api-Presentation-Entities-PlaceArray-1": "PlaceArray",
        "Tfl-Api-Presentation-Entities-PlaceArray-2": "PlaceArray",
        "Tfl-Api-Presentation-Entities-PlaceArray-3": "PlaceArray",
        "Tfl-Api-Presentation-Entities-PlaceArray-4": "PlaceArray",
        "Tfl-Api-Presentation-Entities-PlaceArray-5": "PlaceArray",
        "Tfl-Api-Presentation-Entities-PlaceArray-6": "PlaceArray",
        "Tfl-Api-Presentation-Entities-PlaceArray-7": "PlaceArray",
    },
    "Lift Disruptions": {
        "LiftDisruption": "LiftDisruption",
        "Get200ApplicationJsonResponse": "ArrayOfLiftDisruptions",
    },
    "Journey": {
        "Tfl": "Tfl.Api.Presentation.Entities.Mode",
        "Tfl-10": "Tfl.Api.Presentation.Entities.Identifier",
        "Tfl-11": "Tfl.Api.Common.JourneyPlanner.JpElevation",
        "Tfl-12": "Tfl.Api.Presentation.Entities.JourneyPlanner.Path",
        "Tfl-13": "Tfl.Api.Presentation.Entities.JourneyPlanner.RouteOption",
        "Tfl-14": "Tfl.Api.Presentation.Entities.LineGroup",
        "Tfl-15": "Tfl.Api.Presentation.Entities.LineModeGroup",
        "Tfl-16": "Tfl.Api.Presentation.Entities.AdditionalProperties",
        "Tfl-17": "Tfl.Api.Presentation.Entities.Place",
        "Tfl-18": "Tfl.Api.Presentation.Entities.StopPoint",
        "Tfl-19": "Tfl.Api.Presentation.Entities.RouteSectionNaptanEntrySequence",
        "Tfl-2": "Tfl.Api.Presentation.Entities.PathAttribute",
        "Tfl-20": "Tfl.Api.Presentation.Entities.RouteSection",
        "Tfl-21": "Tfl.Api.Presentation.Entities.Disruption",
        "Tfl-22": "Tfl.Api.Presentation.Entities.JourneyPlanner.PlannedWork",
        "Tfl-23": "Tfl.Api.Presentation.Entities.JourneyPlanner.Leg",
        "Tfl-24": "Tfl.Api.Presentation.Entities.JourneyPlanner.FareTapDetails",
        "Tfl-25": "Tfl.Api.Presentation.Entities.JourneyPlanner.FareTap",
        "Tfl-26": "Tfl.Api.Presentation.Entities.JourneyPlanner.Fare",
        "Tfl-27": "Tfl.Api.Presentation.Entities.JourneyPlanner.FareCaveat",
        "Tfl-28": "Tfl.Api.Presentation.Entities.JourneyPlanner.JourneyFare",
        "Tfl-29": "Tfl.Api.Presentation.Entities.JourneyPlanner.Journey",
        "Tfl-3": "Tfl.Api.Presentation.Entities.InstructionStep",
        "Tfl-30": "Tfl.Api.Presentation.Entities.ValidityPeriod",
        "Tfl-31": "Tfl.Api.Presentation.Entities.LineStatus",
        "Tfl-32": "Tfl.Api.Presentation.Entities.MatchedRoute",
        "Tfl-33": "Tfl.Api.Presentation.Entities.LineServiceTypeInfo",
        "Tfl-34": "Tfl.Api.Presentation.Entities.Line",
        "Tfl-35": "Tfl.Api.Presentation.Entities.JourneyPlanner.JourneyPlannerCycleHireDockingStationData",
        "Tfl-36": "Tfl.Api.Presentation.Entities.JourneyPlanner.TimeAdjustment",
        "Tfl-37": "Tfl.Api.Presentation.Entities.JourneyPlanner.TimeAdjustments",
        "Tfl-38": "Tfl.Api.Presentation.Entities.JourneyPlanner.SearchCriteria",
        "Tfl-39": "Tfl.Api.Presentation.Entities.JourneyPlanner.JourneyVector",
        "Tfl-4": "Tfl.Api.Presentation.Entities.Instruction",
        "Tfl-40": "Tfl.Api.Presentation.Entities.JourneyPlanner.ItineraryResult",
        "Tfl-5": "Tfl.Api.Presentation.Entities.JourneyPlanner.Obstacle",
        "Tfl-6": "Tfl.Api.Presentation.Entities.Point",
        "Tfl-7": "Tfl.Api.Presentation.Entities.PassengerFlow",
        "Tfl-8": "Tfl.Api.Presentation.Entities.TrainLoading",
        "Tfl-9": "Tfl.Api.Presentation.Entities.Crowding",
        "MetaModesGet200ApplicationJsonResponse": "ArrayOfModes",
        "MetaModesGet200TextJsonResponse": "ArrayOfModes",
        "MetaModesGet200ApplicationXmlResponse": "ArrayOfModes",
        "MetaModesGet200TextXmlResponse": "ArrayOfModes",
        "Get200ApplicationJsonResponse": "ObjectResponse",
    },
    "Line": {
        "MetaModesGet200ApplicationJsonResponse": "ArrayOfModes",
        "MetaModesGet200TextJsonResponse": "ArrayOfModes",
        "MetaModesGet200ApplicationXmlResponse": "ArrayOfModes",
        "MetaModesGet200TextXmlResponse": "ArrayOfModes",
        "Get200ApplicationJsonResponse": "ObjectResponse",
        "MetaSeverityGet200ApplicationJsonResponse": "ArrayOfStatusSeverities",
        "MetaSeverityGet200TextJsonResponse": "ArrayOfStatusSeverities",
        "MetaSeverityGet200ApplicationXmlResponse": "ArrayOfStatusSeverities",
        "MetaSeverityGet200TextXmlResponse": "ArrayOfStatusSeverities",
        "MetaDisruptionCategoriesGet200ApplicationJsonResponse": "ArrayOfStrings",
        "MetaDisruptionCategoriesGet200TextJsonResponse": "ArrayOfStrings",
        "MetaDisruptionCategoriesGet200ApplicationXmlResponse": "ArrayOfStrings",
        "MetaDisruptionCategoriesGet200TextXmlResponse": "ArrayOfStrings",
        "MetaServiceTypesGet200ApplicationJsonResponse": "ArrayOfStrings",
        "MetaServiceTypesGet200TextJsonResponse": "ArrayOfStrings",
        "MetaServiceTypesGet200ApplicationXmlResponse": "ArrayOfStrings",
        "MetaServiceTypesGet200TextXmlResponse": "ArrayOfStrings",
        "ids-Get200ApplicationJsonResponse": "ArrayOfLines",
        "ids-Get200TextJsonResponse": "ArrayOfLines",
        "ids-Get200ApplicationXmlResponse": "ArrayOfLines",
        "ids-Get200TextXmlResponse": "ArrayOfLines",
        "Mode-modes-Get200ApplicationJsonResponse": "ArrayOfLines",
        "Mode-modes-Get200TextJsonResponse": "ArrayOfLines",
        "Mode-modes-Get200ApplicationXmlResponse": "ArrayOfLines",
        "Mode-modes-Get200TextXmlResponse": "ArrayOfLines",
        "RouteGet200ApplicationJsonResponse": "ArrayOfLines",
        "RouteGet200TextJsonResponse": "ArrayOfLines",
        "RouteGet200ApplicationXmlResponse": "ArrayOfLines",
        "RouteGet200TextXmlResponse": "ArrayOfLines",
        "ids-RouteGet200ApplicationJsonResponse": "ArrayOfLines",
        "ids-RouteGet200TextJsonResponse": "ArrayOfLines",
        "ids-RouteGet200ApplicationXmlResponse": "ArrayOfLines",
        "ids-RouteGet200TextXmlResponse": "ArrayOfLines",
        "Mode-modes-RouteGet200ApplicationJsonResponse": "ArrayOfLines",
        "Mode-modes-RouteGet200TextJsonResponse": "ArrayOfLines",
        "Mode-modes-RouteGet200ApplicationXmlResponse": "ArrayOfLines",
        "Mode-modes-RouteGet200TextXmlResponse": "ArrayOfLines",
        "ids-Status-startDate-To-endDate-Get200ApplicationJsonResponse": "ArrayOfLines",
        "ids-Status-startDate-To-endDate-Get200TextJsonResponse": "ArrayOfLines",
        "ids-Status-startDate-To-endDate-Get200ApplicationXmlResponse": "ArrayOfLines",
        "ids-Status-startDate-To-endDate-Get200TextXmlResponse": "ArrayOfLines",
        "ids-StatusGet200ApplicationJsonResponse": "ArrayOfLines",
        "ids-StatusGet200TextJsonResponse": "ArrayOfLines",
        "ids-StatusGet200ApplicationXmlResponse": "ArrayOfLines",
        "ids-StatusGet200TextXmlResponse": "ArrayOfLines",
        "Status-severity-Get200ApplicationJsonResponse": "ArrayOfLines",
        "Status-severity-Get200TextJsonResponse": "ArrayOfLines",
        "Status-severity-Get200ApplicationXmlResponse": "ArrayOfLines",
        "Status-severity-Get200TextXmlResponse": "ArrayOfLines",
        "Mode-modes-StatusGet200ApplicationJsonResponse": "ArrayOfLines",
        "Mode-modes-StatusGet200TextJsonResponse": "ArrayOfLines",
        "Mode-modes-StatusGet200ApplicationXmlResponse": "ArrayOfLines",
        "Mode-modes-StatusGet200TextXmlResponse": "ArrayOfLines",
        "id-StopPointsGet200ApplicationJsonResponse": "ArrayOfStopPoints",
        "id-StopPointsGet200TextJsonResponse": "ArrayOfStopPoints",
        "id-StopPointsGet200ApplicationXmlResponse": "ArrayOfStopPoints",
        "id-StopPointsGet200TextXmlResponse": "ArrayOfStopPoints",
        "ids-DisruptionGet200ApplicationJsonResponse": "ArrayOfDisruptions",
        "ids-DisruptionGet200TextJsonResponse": "ArrayOfDisruptions",
        "ids-DisruptionGet200ApplicationXmlResponse": "ArrayOfDisruptions",
        "ids-DisruptionGet200TextXmlResponse": "ArrayOfDisruptions",
        "Mode-modes-DisruptionGet200ApplicationJsonResponse": "ArrayOfDisruptions",
        "Mode-modes-DisruptionGet200TextJsonResponse": "ArrayOfDisruptions",
        "Mode-modes-DisruptionGet200ApplicationXmlResponse": "ArrayOfDisruptions",
        "Mode-modes-DisruptionGet200TextXmlResponse": "ArrayOfDisruptions",
        "ids-Arrivals-stopPointId-Get200ApplicationJsonResponse": "ArrayOfPredictions",
        "ids-Arrivals-stopPointId-Get200TextJsonResponse": "ArrayOfPredictions",
        "ids-Arrivals-stopPointId-Get200ApplicationXmlResponse": "ArrayOfPredictions",
        "ids-Arrivals-stopPointId-Get200TextXmlResponse": "ArrayOfPredictions",
        "ids-ArrivalsGet200ApplicationJsonResponse": "ArrayOfPredictions",
        "ids-ArrivalsGet200TextJsonResponse": "ArrayOfPredictions",
        "ids-ArrivalsGet200ApplicationXmlResponse": "ArrayOfPredictions",
        "ids-ArrivalsGet200TextXmlResponse": "ArrayOfPredictions",
        "Tfl": "Tfl.Api.Presentation.Entities.Mode",
        "Tfl-10": "Tfl.Api.Presentation.Entities.Place",
        "Tfl-11": "Tfl.Api.Presentation.Entities.StopPoint",
        "Tfl-12": "Tfl.Api.Presentation.Entities.RouteSectionNaptanEntrySequence",
        "Tfl-13": "Tfl.Api.Presentation.Entities.RouteSection",
        "Tfl-14": "Tfl.Api.Presentation.Entities.Disruption",
        "Tfl-15": "Tfl.Api.Presentation.Entities.ValidityPeriod",
        "Tfl-16": "Tfl.Api.Presentation.Entities.LineStatus",
        "Tfl-17": "Tfl.Api.Presentation.Entities.MatchedRoute",
        "Tfl-18": "Tfl.Api.Presentation.Entities.LineServiceTypeInfo",
        "Tfl-19": "Tfl.Api.Presentation.Entities.Line",
        "Tfl-2": "Tfl.Api.Presentation.Entities.StatusSeverity",
        "Tfl-20": "Tfl.Api.Presentation.Entities.MatchedStop",
        "Tfl-21": "Tfl.Api.Presentation.Entities.StopPointSequence",
        "Tfl-22": "Tfl.Api.Presentation.Entities.OrderedRoute",
        "Tfl-23": "Tfl.Api.Presentation.Entities.RouteSequence",
        "Tfl-24": "Tfl.Api.Presentation.Entities.LineRouteSection",
        "Tfl-25": "Tfl.Api.Presentation.Entities.MatchedRouteSections",
        "Tfl-26": "Tfl.Api.Presentation.Entities.RouteSearchMatch",
        "Tfl-27": "Tfl.Api.Presentation.Entities.RouteSearchResponse",
        "Tfl-28": "Tfl.Api.Presentation.Entities.Interval",
        "Tfl-29": "Tfl.Api.Presentation.Entities.StationInterval",
        "Tfl-3": "Tfl.Api.Presentation.Entities.PassengerFlow",
        "Tfl-30": "Tfl.Api.Presentation.Entities.KnownJourney",
        "Tfl-31": "Tfl.Api.Presentation.Entities.TwentyFourHourClockTime",
        "Tfl-32": "Tfl.Api.Presentation.Entities.ServiceFrequency",
        "Tfl-33": "Tfl.Api.Presentation.Entities.Period",
        "Tfl-34": "Tfl.Api.Presentation.Entities.Schedule",
        "Tfl-35": "Tfl.Api.Presentation.Entities.TimetableRoute",
        "Tfl-36": "Tfl.Api.Presentation.Entities.Timetable",
        "Tfl-37": "Tfl.Api.Presentation.Entities.Timetables.DisambiguationOption",
        "Tfl-38": "Tfl.Api.Presentation.Entities.Timetables.Disambiguation",
        "Tfl-39": "Tfl.Api.Presentation.Entities.TimetableResponse",
        "Tfl-4": "Tfl.Api.Presentation.Entities.TrainLoading",
        "Tfl-40": "Tfl.Api.Presentation.Entities.PredictionTiming",
        "Tfl-41": "Tfl.Api.Presentation.Entities.Prediction",
        "Tfl-5": "Tfl.Api.Presentation.Entities.Crowding",
        "Tfl-6": "Tfl.Api.Presentation.Entities.Identifier",
        "Tfl-7": "Tfl.Api.Presentation.Entities.LineGroup",
        "Tfl-8": "Tfl.Api.Presentation.Entities.LineModeGroup",
        "Tfl-9": "Tfl.Api.Presentation.Entities.AdditionalProperties",
    },
    "Mode": {
        "Tfl-Api-Presentation-Entities-ActiveServiceTypeArray": "ArrayOfActiveServiceTypes",
        "Tfl.Api.Presentation.Entities.ActiveServiceType": "Tfl.Api.Presentation.Entities.ActiveServiceType",
        "Tfl-Api-Presentation-Entities-ActiveServiceTypeArray-1": "ArrayOfActiveServiceTypes",
        "Tfl-Api-Presentation-Entities-ActiveServiceTypeArray-2": "ArrayOfActiveServiceTypes",
        "Tfl-Api-Presentation-Entities-ActiveServiceTypeArray-3": "ArrayOfActiveServiceTypes",
        "Tfl-Api-Presentation-Entities-PredictionArray-4": "ArrayOfPredictions",
        "Tfl.Api.Presentation.Entities.Prediction": "Tfl.Api.Presentation.Entities.Prediction",
        "Tfl.Api.Presentation.Entities.PredictionTiming": "Tfl.Api.Presentation.Entities.PredictionTiming",
        "Tfl-Api-Presentation-Entities-PredictionArray-5": "ArrayOfPredictions",
        "Tfl-Api-Presentation-Entities-PredictionArray-6": "ArrayOfPredictions",
        "Tfl-Api-Presentation-Entities-PredictionArray-7": "ArrayOfPredictions",
    },
    "Place": {
        "System": "System.Object",
        "MetaCategoriesGet200ApplicationJsonResponse": "ArrayOfPlaceCategories",
        "MetaCategoriesGet200TextJsonResponse": "ArrayOfPlaceCategories",
        "MetaCategoriesGet200ApplicationXmlResponse": "ArrayOfPlaceCategories",
        "MetaCategoriesGet200TextXmlResponse": "ArrayOfPlaceCategories",
        "Get200ApplicationJsonResponse": "ObjectResponse",
        "MetaPlaceTypesGet200ApplicationJsonResponse": "ArrayOfPlaceCategories",
        "MetaPlaceTypesGet200TextJsonResponse": "ArrayOfPlaceCategories",
        "MetaPlaceTypesGet200ApplicationXmlResponse": "ArrayOfPlaceCategories",
        "MetaPlaceTypesGet200TextXmlResponse": "ArrayOfPlaceCategories",
        "Type-types-Get200ApplicationJsonResponse": "ArrayOfPlaces",
        "Type-types-Get200TextJsonResponse": "ArrayOfPlaces",
        "Type-types-Get200ApplicationXmlResponse": "ArrayOfPlaces",
        "Type-types-Get200TextXmlResponse": "ArrayOfPlaces",
        "id-Get200ApplicationJsonResponse": "ArrayOfPlaces",
        "id-Get200TextJsonResponse": "ArrayOfPlaces",
        "id-Get200ApplicationXmlResponse": "ArrayOfPlaces",
        "id-Get200TextXmlResponse": "ArrayOfPlaces",
        "Get200ApplicationJsonResponse-1": "ArrayOfStopPoints",
        "Get200TextJsonResponse": "ArrayOfStopPoints",
        "Get200ApplicationXmlResponse": "ArrayOfStopPoints",
        "Get200TextXmlResponse": "ArrayOfStopPoints",
        "SearchGet200ApplicationJsonResponse": "ArrayOfPlaces",
        "SearchGet200TextJsonResponse": "ArrayOfPlaces",
        "SearchGet200ApplicationXmlResponse": "ArrayOfPlaces",
        "SearchGet200TextXmlResponse": "ArrayOfPlaces",
        "Tfl": "Tfl.Api.Presentation.Entities.PlaceCategory",
        "Tfl-10": "Tfl.Api.Presentation.Entities.StopPoint",
        "Tfl-2": "Tfl.Api.Presentation.Entities.AdditionalProperties",
        "Tfl-3": "Tfl.Api.Presentation.Entities.Place",
        "Tfl-4": "Tfl.Api.Presentation.Entities.PassengerFlow",
        "Tfl-5": "Tfl.Api.Presentation.Entities.TrainLoading",
        "Tfl-6": "Tfl.Api.Presentation.Entities.Crowding",
        "Tfl-7": "Tfl.Api.Presentation.Entities.Identifier",
        "Tfl-8": "Tfl.Api.Presentation.Entities.LineGroup",
        "Tfl-9": "Tfl.Api.Presentation.Entities.LineModeGroup",
    },
    "Road": {
        "System": "System.Data.Spatial.DbGeographyWellKnownValue",
        "System-2": "System.Data.Spatial.DbGeography",
        "System-3": "System.Object",
        "Tfl": "Tfl.Api.Presentation.Entities.RoadCorridor",
        "Tfl-2": "Tfl.Api.Presentation.Entities.StreetSegment",
        "Tfl-3": "Tfl.Api.Presentation.Entities.Street",
        "Tfl-4": "Tfl.Api.Presentation.Entities.RoadProject",
        "Tfl-5": "Tfl.Api.Presentation.Entities.RoadDisruptionLine",
        "Tfl-6": "Tfl.Api.Presentation.Entities.RoadDisruptionImpactArea",
        "Tfl-7": "Tfl.Api.Presentation.Entities.RoadDisruptionSchedule",
        "Tfl-8": "Tfl.Api.Presentation.Entities.RoadDisruption",
        "Tfl-9": "Tfl.Api.Presentation.Entities.StatusSeverity",
        "Get200ApplicationJsonResponse": "ArrayOfRoadCorridors",
        "Get200TextJsonResponse": "ArrayOfRoadCorridors",
        "Get200ApplicationXmlResponse": "ArrayOfRoadCorridors",
        "Get200TextXmlResponse": "ArrayOfRoadCorridors",
        "ids-Get200ApplicationJsonResponse": "ArrayOfRoadCorridors",
        "ids-Get200TextJsonResponse": "ArrayOfRoadCorridors",
        "ids-Get200ApplicationXmlResponse": "ArrayOfRoadCorridors",
        "ids-Get200TextXmlResponse": "ArrayOfRoadCorridors",
        "ids-StatusGet200ApplicationJsonResponse": "ArrayOfRoadCorridors",
        "ids-StatusGet200TextJsonResponse": "ArrayOfRoadCorridors",
        "ids-StatusGet200ApplicationXmlResponse": "ArrayOfRoadCorridors",
        "ids-StatusGet200TextXmlResponse": "ArrayOfRoadCorridors",
        "ids-DisruptionGet200ApplicationJsonResponse": "ArrayOfRoadDisruptions",
        "ids-DisruptionGet200TextJsonResponse": "ArrayOfRoadDisruptions",
        "ids-DisruptionGet200ApplicationXmlResponse": "ArrayOfRoadDisruptions",
        "ids-DisruptionGet200TextXmlResponse": "ArrayOfRoadDisruptions",
        "ids-DisruptionGet200ApplicationGeo-jsonResponse": "ArrayOfRoadDisruptions",
        "MetaCategoriesGet200ApplicationJsonResponse": "ArrayOfStrings",
        "MetaCategoriesGet200TextJsonResponse": "ArrayOfStrings",
        "MetaCategoriesGet200ApplicationXmlResponse": "ArrayOfStrings",
        "MetaCategoriesGet200TextXmlResponse": "ArrayOfStrings",
        "MetaSeveritiesGet200ApplicationJsonResponse": "ArrayOfStatusSeverities",
        "MetaSeveritiesGet200TextJsonResponse": "ArrayOfStatusSeverities",
        "MetaSeveritiesGet200ApplicationXmlResponse": "ArrayOfStatusSeverities",
        "MetaSeveritiesGet200TextXmlResponse": "ArrayOfStatusSeverities",
    },
    "Search": {
        "Tfl": "Tfl.Api.Presentation.Entities.SearchMatch",
        "Tfl-2": "Tfl.Api.Presentation.Entities.SearchResponse",
        "MetaSearchProvidersGet200ApplicationJsonResponse": "ArrayOfStrings",
        "MetaSearchProvidersGet200TextJsonResponse": "ArrayOfStrings",
        "MetaSearchProvidersGet200ApplicationXmlResponse": "ArrayOfStrings",
        "MetaSearchProvidersGet200TextXmlResponse": "ArrayOfStrings",
        "MetaCategoriesGet200ApplicationJsonResponse": "ArrayOfStrings",
        "MetaCategoriesGet200TextJsonResponse": "ArrayOfStrings",
        "MetaCategoriesGet200ApplicationXmlResponse": "ArrayOfStrings",
        "MetaCategoriesGet200TextXmlResponse": "ArrayOfStrings",
        "MetaSortsGet200ApplicationJsonResponse": "ArrayOfStrings",
        "MetaSortsGet200TextJsonResponse": "ArrayOfStrings",
        "MetaSortsGet200ApplicationXmlResponse": "ArrayOfStrings",
        "MetaSortsGet200TextXmlResponse": "ArrayOfStrings",
    },
    "StopPoint": {
        "System": "System.Object",
        "Tfl": "Tfl.Api.Presentation.Entities.StopPointCategory",
        "Tfl-10": "Tfl.Api.Presentation.Entities.Place",
        "Tfl-11": "Tfl.Api.Presentation.Entities.StopPoint",
        "Tfl-12": "Tfl.Api.Presentation.Entities.LineServiceTypeInfo",
        "Tfl-13": "Tfl.Api.Presentation.Entities.LineSpecificServiceType",
        "Tfl-14": "Tfl.Api.Presentation.Entities.LineServiceType",
        "Tfl-15": "Tfl.Api.Presentation.Entities.PredictionTiming",
        "Tfl-16": "Tfl.Api.Presentation.Entities.Prediction",
        "Tfl-17": "Tfl.Api.Presentation.Entities.ArrivalDeparture",
        "Tfl-18": "Tfl.Api.Presentation.Entities.StopPointRouteSection",
        "Tfl-19": "Tfl.Api.Presentation.Entities.DisruptedPoint",
        "Tfl-2": "Tfl.Api.Presentation.Entities.Mode",
        "Tfl-20": "Tfl.Api.Presentation.Entities.StopPointsResponse",
        "Tfl-21": "Tfl.Api.Presentation.Entities.SearchMatch",
        "Tfl-22": "Tfl.Api.Presentation.Entities.SearchResponse",
        "Tfl-3": "Tfl.Api.Presentation.Entities.PassengerFlow",
        "Tfl-4": "Tfl.Api.Presentation.Entities.TrainLoading",
        "Tfl-5": "Tfl.Api.Presentation.Entities.Crowding",
        "Tfl-6": "Tfl.Api.Presentation.Entities.Identifier",
        "Tfl-7": "Tfl.Api.Presentation.Entities.LineGroup",
        "Tfl-8": "Tfl.Api.Presentation.Entities.LineModeGroup",
        "Tfl-9": "Tfl.Api.Presentation.Entities.AdditionalProperties",
    },
    "Vehicle": {
        "Tfl": "Tfl.Api.Presentation.Entities.PredictionTiming",
        "Tfl-2": "Tfl.Api.Presentation.Entities.Prediction",
        "Tfl-3": "Tfl.Api.Presentation.Entities.VehicleMatch",
        "ids-ArrivalsGet200ApplicationJsonResponse": "ArrayOfPredictions",
        "ids-ArrivalsGet200TextJsonResponse": "ArrayOfPredictions",
        "ids-ArrivalsGet200ApplicationXmlResponse": "ArrayOfPredictions",
        "ids-ArrivalsGet200TextXmlResponse": "ArrayOfPredictions",
    },
    "crowding": {},
    "occupancy": {
        "Tfl": "Tfl.Api.Presentation.Entities.Bay",
        "Tfl-2": "Tfl.Api.Presentation.Entities.CarParkOccupancy",
        "Tfl-3": "Tfl.Api.Presentation.Entities.ChargeConnectorOccupancy",
        "Tfl-4": "Tfl.Api.Presentation.Entities.BikePointOccupancy",
    },
}


# Helper functions
def sanitize_name(name: str) -> str:
    """
    Sanitize class names or field names to ensure they are valid Python identifiers.
    1. Replace invalid characters (like hyphens) with underscores.
    2. Extract the portion after the last underscore for more concise names.
    3. Prepend 'Model_' if the name starts with a number or is a Python keyword.
    """
    # Replace invalid characters (like hyphens) with underscores
    sanitized = re.sub(r"[^a-zA-Z0-9_]", "_", name)

    # Extract the portion after the last underscore for concise names
    sanitized = sanitized.split("_")[-1]

    # Always prepend 'Model_' to ensure names are valid and don't conflict with Python keywords
    if sanitized[0].isdigit() or keyword.iskeyword(sanitized):
        sanitized = f"Model_{sanitized}"

    return sanitized


def update_refs(obj: Any, entity_mapping: Dict[str, str]):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "$ref" and value.split("/")[-1] in entity_mapping:
                obj[key] = value.replace(value.split("/")[-1], entity_mapping[value.split("/")[-1]])
            else:
                update_refs(value, entity_mapping)
    elif isinstance(obj, list):
        for item in obj:
            update_refs(item, entity_mapping)


# Update entities and references
def update_entities(spec: Dict[str, Any], api_name: str, pydantic_names: Dict[str, str]) -> None:
    if api_name not in tfl_mappings:
        return

    entity_mapping = tfl_mappings[api_name]
    components = spec.get("components", {}).get("schemas", {})

    # Sanitize old and new names to match how they will be used in the models
    sanitized_entity_mapping = {old_name: sanitize_name(new_name) for old_name, new_name in entity_mapping.items()}

    # Rename entities in the schema components
    for old_name, new_name in sanitized_entity_mapping.items():
        if old_name in components:
            components[new_name] = components.pop(old_name)
            pydantic_names[old_name] = new_name

    # Update references recursively in the spec
    update_refs(spec, sanitized_entity_mapping)


def create_enum_class(enum_name: str, enum_values: List[Any]) -> Type[Enum]:
    """Dynamically create a Pydantic Enum class for the given enum values."""

    def clean_enum_name(value: str) -> str:
        # Replace spaces and special characters with underscores and capitalize all letters
        return re.sub(r"\W|^(?=\d)", "_", value).strip("_").replace("-", "_").upper()

    # Create a dictionary with cleaned enum names as keys and the original values as values
    enum_dict = {clean_enum_name(str(v)): v for v in enum_values}

    # Dynamically create the Enum class
    return Enum(enum_name, enum_dict)


def map_type(
    field_spec: Dict[str, Any], field_name: str, components: Dict[str, Any], models: Dict[str, Type[BaseModel]]
) -> Any:
    if "$ref" in field_spec:
        # Handle references
        return sanitize_name(field_spec["$ref"].split("/")[-1])

    openapi_type = field_spec.get("type", "Any")

    # Handle enums with mixed types
    if "enum" in field_spec:
        enum_values = field_spec["enum"]
        # Capitalize just the first letter of the field name, leave the rest as is
        cap_field_name = field_name[0].upper() + field_name[1:]
        enum_name = f"{cap_field_name}Enum"
        # Dynamically create an enum class and return it
        return create_enum_class(enum_name, enum_values)

    # Handle arrays
    if openapi_type == "array":
        # Ensure that 'items' exist for arrays, fallback to Any if missing
        items_spec = field_spec.get("items", {})
        if items_spec:
            return List[map_type(items_spec, field_name, components, models)]
        else:
            logging.warning(f"'items' missing in array definition, using Any")
            return List[Any]

    # Map standard OpenAPI types to Python types
    return {
        "string": str,
        "integer": int,
        "boolean": bool,
        "number": float,
        "object": dict,
    }.get(openapi_type, Any)


# Create Pydantic models
def create_pydantic_models(components: Dict[str, Any], models: Dict[str, Type[BaseModel]]) -> None:
    # First pass: create object models
    for model_name, model_spec in components.items():
        sanitized_name = sanitize_name(model_name)  # Ensure the model name is valid
        if model_spec.get("type") == "object" and "properties" in model_spec:
            # Handle object models first
            fields = {}
            required_fields = model_spec.get("required", [])
            for field_name, field_spec in model_spec["properties"].items():
                field_type = map_type(field_spec, field_name, components, models)  # Map the OpenAPI type to Python type
                sanitized_field_name = sanitize_field_name(field_name)
                if field_name in required_fields:
                    fields[sanitized_field_name] = (field_type, Field(..., alias=field_name))
                else:
                    fields[sanitized_field_name] = (Optional[field_type], Field(None, alias=field_name))
            models[sanitized_name] = create_model(sanitized_name, **fields)
            logging.info(f"Created object model: {sanitized_name}")

    # Second pass: handle array models referencing the object models
    for model_name, model_spec in components.items():
        sanitized_name = sanitize_name(model_name)
        if model_spec.get("type") == "array":
            # Handle array models
            items_spec = model_spec.get("items")
            if "$ref" in items_spec:
                # Handle reference in 'items'
                ref_model_name = sanitize_name(items_spec["$ref"].split("/")[-1])
                if ref_model_name not in models:
                    raise KeyError(
                        f"Referenced model '{ref_model_name}' not found while creating array '{sanitized_name}'"
                    )
                models[sanitized_name] = List[models[ref_model_name]]  # Create List type for array items
                logging.info(f"Created array model: {sanitized_name} -> List[{ref_model_name}]")
            else:
                # Fallback if 'items' is missing or doesn't have a reference
                models[sanitized_name] = List[Any]
                logging.warning(f"Array model {sanitized_name} has no valid 'items' reference. Using List[Any].")


# Save models and config to files
def determine_typing_imports(model_fields, models, circular_models, is_list_model=False):
    """Determine the necessary typing imports based on the model's fields."""
    import_set = set()  # Core imports like BaseModel will be handled separately

    # Always add List for list models
    if is_list_model:
        import_set.add("from typing import List")

    for field in model_fields.values():
        field_annotation = get_type_str(field.annotation, models)
        if "Optional" in field_annotation:
            import_set.add("from typing import Optional")
        if "List" in field_annotation:
            import_set.add("from typing import List")
        if "Union" in field_annotation:
            import_set.add("from typing import Union")
        if field_annotation in circular_models:
            import_set.add("from typing import ForwardRef")

    return import_set


def save_models(
    models: Dict[str, Union[Type[BaseModel], Type[List]]],
    base_path: str,
    dependency_graph: Dict[str, Set[str]],
    circular_models: Set[str],
):
    models_dir = os.path.join(base_path, "models")
    os.makedirs(models_dir, exist_ok=True)

    init_file = os.path.join(models_dir, "__init__.py")
    with open(init_file, "w") as init_f:

        for model_name, model in models.items():
            save_model_file(model_name, model, models, models_dir, dependency_graph, circular_models, init_f)

        init_f.write(f"\n__all__ = [\n    {',\n    '.join(models.keys())}\n]\n")

    # Write enums after saving the models
    write_enum_files(models, models_dir)


def save_model_file(
    model_name: str,
    model: Any,
    models: Dict[str, Type[BaseModel]],
    models_dir: str,
    dependency_graph: Dict[str, Set[str]],
    circular_models: Set[str],
    init_f,
):
    sanitized_model_name = sanitize_name(model_name)
    model_file = os.path.join(models_dir, f"{sanitized_model_name}.py")

    with open(model_file, "w") as mf:
        mf.write("from pydantic import BaseModel, Field\n")

        if is_list_model(model):
            handle_list_model(mf, model, models, dependency_graph, circular_models, sanitized_model_name)
        else:
            handle_regular_model(mf, model, models, dependency_graph, circular_models, sanitized_model_name)

        init_f.write(f"from .{sanitized_model_name} import {sanitized_model_name}\n")


def is_list_model(model: Any) -> bool:
    return hasattr(model, "__origin__") and model.__origin__ is list


def handle_list_model(mf, model, models, dependency_graph, circular_models, sanitized_model_name):
    inner_type = model.__args__[0]

    # Determine necessary imports for list models
    import_set = determine_typing_imports({}, models, circular_models, is_list_model=True)

    type_imports = set()

    if hasattr(inner_type, "__name__") and inner_type.__name__ not in {"Optional", "List", "Union"}:
        inner_model_name = sanitize_name(inner_type.__name__)
        if inner_model_name in dependency_graph:
            import_set.add(f"from .{inner_model_name} import {inner_model_name}")
        else:
            type_imports.add(inner_type.__name__)

    if type_imports:
        import_set.add(f"from typing import {', '.join(type_imports)}")

    # Write imports
    mf.write("\n".join(sorted(import_set)) + "\n\n\n")

    # Define the list model using RootModel
    mf.write(f"class {sanitized_model_name}(BaseModel):\n")
    mf.write(f"    data: List[{inner_type.__name__}] = Field(..., alias='data')\n")

    mf.write(f"\n    class Config:\n")
    mf.write("        from_attributes = True\n")


def handle_regular_model(mf, model, models, dependency_graph, circular_models, sanitized_model_name):
    if hasattr(model, "model_fields"):
        # Determine necessary imports for regular models
        import_set = determine_typing_imports(model.model_fields, models, circular_models)

        # Write imports for referenced models
        referenced_models = dependency_graph.get(sanitized_model_name, set())
        for ref_model in referenced_models:
            if ref_model != sanitized_model_name and ref_model not in {"Optional", "List", "Union"}:
                import_set.add(f"from .{ref_model} import {ref_model}")

        # Add Enum imports
        import_set.update(find_enum_imports(model, models))

        # Write imports
        mf.write("\n".join(sorted(import_set)) + "\n\n\n")

        # Write class definition
        mf.write(f"class {sanitized_model_name}(BaseModel):\n")
        write_model_fields(mf, model, models, circular_models, sanitized_model_name)

        # Pydantic model config
        mf.write("\n    class Config:\n")
        mf.write("        from_attributes = True\n")

        # Add model_rebuild() if circular dependencies exist
        if sanitized_model_name in circular_models:
            mf.write(f"\n{sanitized_model_name}.model_rebuild()\n")


def find_enum_imports(model: Any, models: Dict[str, Type[BaseModel]]) -> Set[str]:
    """Find all enum imports in the model fields."""
    import_set = set()
    for field_name, field in model.model_fields.items():
        inner_types = extract_inner_types(field.annotation)
        for inner_type in inner_types:
            if isinstance(inner_type, type) and issubclass(inner_type, Enum):
                import_set.add(f"from .{inner_type.__name__} import {inner_type.__name__}")
    return import_set


def write_model_fields(mf, model, models, circular_models, sanitized_model_name):
    """Write the fields for the model."""
    for field_name, field in model.model_fields.items():
        sanitized_field_name = sanitize_field_name(field_name)

        # Extract the inner types (handles Optional, List, and Union)
        inner_types = extract_inner_types(field.annotation)

        # Check if any inner type is a circular reference
        circular_reference = any(
            (isinstance(inner_type, ForwardRef) and inner_type.__forward_arg__ in circular_models)
            or (isinstance(inner_type, str) and inner_type in circular_models)
            or (hasattr(inner_type, "__name__") and inner_type.__name__ in circular_models)
            for inner_type in inner_types
        )

        # Get the type string for the field
        field_type = get_type_str(field.annotation, models)

        # Handle circular dependencies: if circular, use forward reference
        if circular_reference:
            mf.write(f"    {sanitized_field_name}: '{field_type}' = Field(None, alias='{field.alias}')\n")
        else:
            mf.write(f"    {sanitized_field_name}: {field_type} = Field(None, alias='{field.alias}')\n")


def write_enum_files(models: Dict[str, Type[BaseModel]], models_dir: str):
    """Write enum files directly from the model's fields."""
    for model in models.values():
        if hasattr(model, "model_fields"):
            for field in model.model_fields.values():
                inner_types = extract_inner_types(field.annotation)
                for inner_type in inner_types:
                    if isinstance(inner_type, type) and issubclass(inner_type, Enum):
                        enum_name = inner_type.__name__
                        enum_file = os.path.join(models_dir, f"{enum_name}.py")
                        with open(enum_file, "w") as ef:
                            ef.write("from enum import Enum\n\n\n")
                            ef.write(f"class {enum_name}(Enum):\n")
                            for enum_member in inner_type:
                                ef.write(f"    {enum_member.name} = '{enum_member.value}'\n")


def sanitize_field_name(field_name: str) -> str:
    """Sanitize field names that are Python reserved keywords."""
    if keyword.iskeyword(field_name):
        return f"{field_name}_field"  # Append '_field' to reserved keywords
    return field_name


def get_type_str(annotation: Any, models: Dict[str, Type[BaseModel]]) -> str:
    """Convert the annotation to a valid Python type string for writing to a file, handling model references."""
    if isinstance(annotation, ForwardRef):
        # Handle ForwardRef directly by returning the forward-referenced name
        return annotation.__forward_arg__

    if isinstance(annotation, type):
        # Handle basic types (e.g., int, str, float)
        return annotation.__name__

    elif hasattr(annotation, "__origin__"):
        origin = annotation.__origin__
        args = annotation.__args__

        # Handle List (e.g., List[str], List[Casualty])
        if origin is list or origin is List:
            inner_type = get_type_str(args[0], models)
            return f"List[{inner_type}]"

        # Handle Dict (e.g., Dict[str, int])
        elif origin is dict or origin is Dict:
            key_type = get_type_str(args[0], models)
            value_type = get_type_str(args[1], models)
            return f"Dict[{key_type}, {value_type}]"

        # Handle Optional and Union (e.g., Optional[int], Union[str, int])
        elif origin is Union:
            if len(args) == 2 and args[1] is type(None):
                # It's an Optional type
                return f"Optional[{get_type_str(args[0], models)}]"
            else:
                # General Union type
                inner_types = ", ".join(get_type_str(arg, models) for arg in args)
                return f"Union[{inner_types}]"

    elif hasattr(annotation, "__name__") and annotation.__name__ in models:
        # Handle references to other models (e.g., Casualty)
        return annotation.__name__

    return "Any"


def save_config(config: Dict[str, Dict[str, str]], file_path: str):
    with open(file_path, "w") as f:
        json.dump(config, f, indent=4)


def create_mermaid_class_diagram(dependency_graph: Dict[str, Set[str]], output_file: str):
    with open(output_file, "w") as f:
        f.write("classDiagram\n")
        for model, dependencies in dependency_graph.items():
            for dep in dependencies:
                f.write(f"    {model} --> {dep}\n")


# Dependency handling and circular references
def extract_inner_types(annotation: Any) -> List[Any]:
    """Recursively extract inner types from nested generics (e.g., Optional[List[ForwardRef]])"""
    inner_types = []
    origin = get_origin(annotation)

    # If it's a Union (i.e., Optional), extract the non-None type
    if origin is Union:
        for arg in get_args(annotation):
            if arg is not type(None):  # Ignore NoneType in Optional
                inner_types.extend(extract_inner_types(arg))
    # If it's a List or another generic type, extract its arguments
    elif origin in {list, List, Optional}:
        inner_types.extend(extract_inner_types(get_args(annotation)[0]))
    # Base case: return the annotation itself
    else:
        inner_types.append(annotation)

    return inner_types


def build_dependency_graph(models: Dict[str, Union[Type[BaseModel], Type[List]]]) -> Dict[str, Set[str]]:
    """Build a dependency graph where each model depends on other models."""
    graph = defaultdict(set)

    for model_name, model in models.items():
        if isinstance(model, type) and hasattr(model, "model_fields"):
            # Iterate over each field in the model
            for field in model.model_fields.values():
                # Recursively unwrap and extract the inner types
                inner_types = extract_inner_types(field.annotation)

                for inner_type in inner_types:
                    # Handle ForwardRef (string-based references)
                    if isinstance(inner_type, ForwardRef):
                        graph[model_name].add(inner_type.__forward_arg__)

                    # Handle direct model references
                    elif hasattr(inner_type, "__name__") and inner_type.__name__ in models:
                        graph[model_name].add(sanitize_name(inner_type.__name__))

                    # If it's a generic type, keep unwrapping
                    elif hasattr(inner_type, "__origin__"):
                        nested_types = extract_inner_types(inner_type)
                        for nested_type in nested_types:
                            if isinstance(nested_type, ForwardRef):
                                graph[model_name].add(nested_type.__forward_arg__)
                            elif hasattr(nested_type, "__name__") and nested_type.__name__ in models:
                                graph[model_name].add(sanitize_name(nested_type.__name__))

        # Handle List models (arrays)
        elif hasattr(model, "__origin__") and model.__origin__ is list:
            inner_type = model.__args__[0]
            if hasattr(inner_type, "__name__") and inner_type.__name__ in models:
                graph[model_name].add(sanitize_name(inner_type.__name__))

    return graph


def handle_dependencies(models: Dict[str, Type[BaseModel]]):
    graph = build_dependency_graph(models)
    sorted_models = topological_sort(graph)
    circular_models = detect_circular_dependencies(graph)
    break_circular_dependencies(models, circular_models)
    return graph, circular_models


def topological_sort(graph: Dict[str, Set[str]]) -> List[str]:
    # Exclude Python built-in types from the graph
    built_in_types = {"str", "int", "float", "bool", "List", "Dict", "Optional", "Union", "Any"}

    # Filter out built-in types from the graph
    in_degree = {model: 0 for model in graph if model not in built_in_types}

    for model, deps in graph.items():
        if model in built_in_types:
            continue  # Skip built-in types

        for dep in deps:
            if dep not in built_in_types:
                if dep not in in_degree:
                    in_degree[dep] = 0
                in_degree[dep] += 1

    # Initialize the queue with nodes that have an in-degree of 0
    queue = deque([model for model in in_degree if in_degree[model] == 0])
    sorted_models = []

    while queue:
        model = queue.popleft()
        sorted_models.append(model)
        for dep in graph[model]:
            if dep in built_in_types:
                continue  # Skip built-in types
            in_degree[dep] -= 1
            if in_degree[dep] == 0:
                queue.append(dep)

    if len(sorted_models) != len(in_degree):
        missing_models = set(in_degree.keys()) - set(sorted_models)
        logging.warning(f"Circular dependencies detected among models: {missing_models}")
        sorted_models.extend(missing_models)

    return sorted_models


def detect_circular_dependencies(graph: Dict[str, Set[str]]) -> Set[str]:
    circular_models = set()
    visited = set()
    stack = set()

    # Use a copy of the graph's keys to avoid modifying the dictionary during iteration
    def visit(model: str):
        if model in visited:
            return
        if model in stack:
            circular_models.add(model)
            return
        stack.add(model)
        for dep in graph.get(model, []):
            visit(dep)
        stack.remove(model)
        visited.add(model)

    # Iterate over a copy of the graph's keys
    for model in list(graph.keys()):
        visit(model)

    return circular_models


def rebuild_annotation_with_inner_types(original_annotation: Any, inner_types: List[Any]) -> Any:
    origin = get_origin(original_annotation)
    if origin is Union:
        # Rebuild Union (e.g., Optional) with the new inner types
        return Union[tuple(inner_types)]
    elif origin in {list, List}:
        # Rebuild List with the new inner types
        return List[inner_types[0]]
    elif origin in {dict, Dict}:
        # Rebuild Dict with the new key-value types
        return Dict[inner_types[0], inner_types[1]]
    # If it's not a generic, just return the updated type
    return inner_types[0]


def break_circular_dependencies(models: Dict[str, Type[BaseModel]], circular_models: Set[str]):
    for model_name in circular_models:
        for field_name, field in models[model_name].model_fields.items():
            # Extract the inner types (e.g., the actual model or type) from the field annotation
            inner_types = extract_inner_types(field.annotation)

            # Check for circular dependencies in the extracted inner types
            for i, inner_type in enumerate(inner_types):
                if isinstance(inner_type, type) and inner_type.__name__ in circular_models:
                    # Replace the circular dependency with ForwardRef while keeping the surrounding structure
                    inner_types[i] = ForwardRef(inner_type.__name__)

            # Rebuild the field annotation using the updated inner types, preserving any Optional/List structure
            field.annotation = rebuild_annotation_with_inner_types(field.annotation, inner_types)


# Load OpenAPI specs
def load_specs(folder_path: str) -> List[Dict[str, Any]]:
    return [json.load(open(os.path.join(folder_path, f))) for f in os.listdir(folder_path) if f.endswith(".json")]


def get_api_name(spec: Dict[str, Any]) -> str:
    return spec["info"]["title"]


# Combine components and paths from all OpenAPI specs
def combine_components_and_paths(specs: List[Dict[str, Any]], pydantic_names: Dict[str, str]) -> Dict[str, Any]:
    combined_components = {}
    combined_paths = {}

    for spec in specs:
        api_name = get_api_name(spec)
        logging.info(f"Processing {api_name}")
        update_entities(spec, api_name, pydantic_names)
        combined_components.update(spec.get("components", {}).get("schemas", {}))

    return combined_components


def are_models_equal(model1: Type[BaseModel], model2: Type[BaseModel]) -> bool:
    """Check if two Pydantic models are equal based on their fields and types."""
    fields1 = {name: str(field.annotation) for name, field in model1.model_fields.items()}
    fields2 = {name: str(field.annotation) for name, field in model2.model_fields.items()}
    return fields1 == fields2


def deduplicate_models(
    models: Dict[str, Union[Type[BaseModel], Type[List]]]
) -> Dict[str, Union[Type[BaseModel], Type[List]]]:
    """Deduplicate models by removing models with the same content."""
    deduplicated_models = {}
    reference_map = {}

    # Compare models to detect duplicates
    for model_name, model in models.items():
        found_duplicate = False

        # Compare with already deduplicated models
        for dedup_model_name, dedup_model in deduplicated_models.items():
            if isinstance(model, type) and isinstance(dedup_model, type):
                # Compare Pydantic models
                if are_models_equal(model, dedup_model):
                    reference_map[model_name] = dedup_model_name
                    found_duplicate = True
                    break

            # Handle List models separately by comparing their inner types
            model_origin = get_origin(model)
            dedup_model_origin = get_origin(dedup_model)

            if model_origin in {list, List} and dedup_model_origin in {list, List}:
                model_inner_type = get_args(model)[0]
                dedup_inner_type = get_args(dedup_model)[0]

                # If the inner types of the lists are the same, consider them duplicates
                if model_inner_type == dedup_inner_type:
                    reference_map[model_name] = dedup_model_name
                    found_duplicate = True
                    break

        # If no duplicate found, keep the model
        if not found_duplicate:
            deduplicated_models[model_name] = model

    # Return the deduplicated models and reference map
    return deduplicated_models, reference_map


def update_model_references(
    models: Dict[str, Union[Type[BaseModel], Type[List]]], reference_map: Dict[str, str]
) -> Dict[str, Union[Type[BaseModel], Type[List]]]:
    """Update references in models based on the deduplication reference map."""
    updated_models = {}

    for model_name, model in models.items():
        # If the model was deduplicated, update its reference
        if model_name in reference_map:
            dedup_model_name = reference_map[model_name]
            updated_models[model_name] = models[dedup_model_name]
        else:
            updated_models[model_name] = model

    return updated_models


# Main function
def main(base_path: str):
    logging.info("Loading OpenAPI specs...")
    specs = load_specs(base_path)

    logging.info("Generating components...")
    pydantic_names = {}
    combined_components = combine_components_and_paths(specs, pydantic_names)

    logging.info("Generating Pydantic models...")
    models = {}
    create_pydantic_models(combined_components, models)

    # Deduplicate models before saving them
    logging.info("Deduplicating models...")
    deduplicated_models, reference_map = deduplicate_models(models)

    # Update model references
    models = update_model_references(deduplicated_models, reference_map)

    logging.info("Handling dependencies...")
    dependency_graph, circular_models = handle_dependencies(models)

    # Now save the deduplicated models
    logging.info("Saving models to files...")
    save_models(deduplicated_models, base_path, dependency_graph, circular_models)

    # If you still want to save the config and diagram, you can uncomment these parts:
    # logging.info("Saving configuration file...")
    # config = {"sample_endpoint": {"uri": "/sample", "model": "SampleModel"}}  # Simplified config
    # save_config(config, os.path.join(base_path, "config.json"))

    logging.info("Creating Mermaid class diagram...")
    create_mermaid_class_diagram(dependency_graph, os.path.join(base_path, "class_diagram.mmd"))

    logging.info("Processing complete.")


if __name__ == "__main__":
    main("OpenAPI_specs/")
