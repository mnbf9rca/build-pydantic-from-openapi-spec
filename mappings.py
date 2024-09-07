# mappings from https://techforum.tfl.gov.uk/t/swagger-file-outdated/2085/8
# modified to be a dictionary of dictionaries
# I then added specific response codes e.g. ids-Get200ApplicationJsonResponse as keys
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
        "MetaModesGet200ApplicationJsonResponse": "ModeArray",
        "MetaModesGet200TextJsonResponse": "ModeArray",
        "MetaModesGet200ApplicationXmlResponse": "ModeArray",
        "MetaModesGet200TextXmlResponse": "ModeArray",
        "Get200ApplicationJsonResponse": "ObjectResponse",
    },
    "Line": {
        "MetaModesGet200ApplicationJsonResponse": "ModeArray",
        "MetaModesGet200TextJsonResponse": "ModeArray",
        "MetaModesGet200ApplicationXmlResponse": "ModeArray",
        "MetaModesGet200TextXmlResponse": "ModeArray",
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
        "ids-Get200ApplicationJsonResponse": "ArrayOfLine",
        "ids-Get200TextJsonResponse": "ArrayOfLine",
        "ids-Get200ApplicationXmlResponse": "ArrayOfLine",
        "ids-Get200TextXmlResponse": "ArrayOfLine",
        "Mode-modes-Get200ApplicationJsonResponse": "ArrayOfLine",
        "Mode-modes-Get200TextJsonResponse": "ArrayOfLine",
        "Mode-modes-Get200ApplicationXmlResponse": "ArrayOfLine",
        "Mode-modes-Get200TextXmlResponse": "ArrayOfLine",
        "RouteGet200ApplicationJsonResponse": "ArrayOfLine",
        "RouteGet200TextJsonResponse": "ArrayOfLine",
        "RouteGet200ApplicationXmlResponse": "ArrayOfLine",
        "RouteGet200TextXmlResponse": "ArrayOfLine",
        "ids-RouteGet200ApplicationJsonResponse": "ArrayOfLine",
        "ids-RouteGet200TextJsonResponse": "ArrayOfLine",
        "ids-RouteGet200ApplicationXmlResponse": "ArrayOfLine",
        "ids-RouteGet200TextXmlResponse": "ArrayOfLine",
        "Mode-modes-RouteGet200ApplicationJsonResponse": "ArrayOfLine",
        "Mode-modes-RouteGet200TextJsonResponse": "ArrayOfLine",
        "Mode-modes-RouteGet200ApplicationXmlResponse": "ArrayOfLine",
        "Mode-modes-RouteGet200TextXmlResponse": "ArrayOfLine",
        "ids-Status-startDate-To-endDate-Get200ApplicationJsonResponse": "ArrayOfLine",
        "ids-Status-startDate-To-endDate-Get200TextJsonResponse": "ArrayOfLine",
        "ids-Status-startDate-To-endDate-Get200ApplicationXmlResponse": "ArrayOfLine",
        "ids-Status-startDate-To-endDate-Get200TextXmlResponse": "ArrayOfLine",
        "ids-StatusGet200ApplicationJsonResponse": "ArrayOfLine",
        "ids-StatusGet200TextJsonResponse": "ArrayOfLine",
        "ids-StatusGet200ApplicationXmlResponse": "ArrayOfLine",
        "ids-StatusGet200TextXmlResponse": "ArrayOfLine",
        "Status-severity-Get200ApplicationJsonResponse": "ArrayOfLine",
        "Status-severity-Get200TextJsonResponse": "ArrayOfLine",
        "Status-severity-Get200ApplicationXmlResponse": "ArrayOfLine",
        "Status-severity-Get200TextXmlResponse": "ArrayOfLine",
        "Mode-modes-StatusGet200ApplicationJsonResponse": "ArrayOfLine",
        "Mode-modes-StatusGet200TextJsonResponse": "ArrayOfLine",
        "Mode-modes-StatusGet200ApplicationXmlResponse": "ArrayOfLine",
        "Mode-modes-StatusGet200TextXmlResponse": "ArrayOfLine",
        "id-StopPointsGet200ApplicationJsonResponse": "StopPointArray",
        "id-StopPointsGet200TextJsonResponse": "StopPointArray",
        "id-StopPointsGet200ApplicationXmlResponse": "StopPointArray",
        "id-StopPointsGet200TextXmlResponse": "StopPointArray",
        "ids-DisruptionGet200ApplicationJsonResponse": "ArrayOfDisruptions",
        "ids-DisruptionGet200TextJsonResponse": "ArrayOfDisruptions",
        "ids-DisruptionGet200ApplicationXmlResponse": "ArrayOfDisruptions",
        "ids-DisruptionGet200TextXmlResponse": "ArrayOfDisruptions",
        "Mode-modes-DisruptionGet200ApplicationJsonResponse": "ArrayOfDisruptions",
        "Mode-modes-DisruptionGet200TextJsonResponse": "ArrayOfDisruptions",
        "Mode-modes-DisruptionGet200ApplicationXmlResponse": "ArrayOfDisruptions",
        "Mode-modes-DisruptionGet200TextXmlResponse": "ArrayOfDisruptions",
        "ids-Arrivals-stopPointId-Get200ApplicationJsonResponse": "PredictionArray",
        "ids-Arrivals-stopPointId-Get200TextJsonResponse": "PredictionArray",
        "ids-Arrivals-stopPointId-Get200ApplicationXmlResponse": "PredictionArray",
        "ids-Arrivals-stopPointId-Get200TextXmlResponse": "PredictionArray",
        "ids-ArrivalsGet200ApplicationJsonResponse": "PredictionArray",
        "ids-ArrivalsGet200TextJsonResponse": "PredictionArray",
        "ids-ArrivalsGet200ApplicationXmlResponse": "PredictionArray",
        "ids-ArrivalsGet200TextXmlResponse": "PredictionArray",
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
        "Tfl-Api-Presentation-Entities-PredictionArray-4": "PredictionArray",
        "Tfl.Api.Presentation.Entities.Prediction": "Tfl.Api.Presentation.Entities.Prediction",
        "Tfl.Api.Presentation.Entities.PredictionTiming": "Tfl.Api.Presentation.Entities.PredictionTiming",
        "Tfl-Api-Presentation-Entities-PredictionArray-5": "PredictionArray",
        "Tfl-Api-Presentation-Entities-PredictionArray-6": "PredictionArray",
        "Tfl-Api-Presentation-Entities-PredictionArray-7": "PredictionArray",
    },
    "Place": {
        "System": "System.Object",
        "MetaCategoriesGet200ApplicationJsonResponse": "PlaceCategoryArray",
        "MetaCategoriesGet200TextJsonResponse": "PlaceCategoryArray",
        "MetaCategoriesGet200ApplicationXmlResponse": "PlaceCategoryArray",
        "MetaCategoriesGet200TextXmlResponse": "PlaceCategoryArray",
        "Get200ApplicationJsonResponse": "ObjectResponse",
        "MetaPlaceTypesGet200ApplicationJsonResponse": "PlaceCategoryArray",
        "MetaPlaceTypesGet200TextJsonResponse": "PlaceCategoryArray",
        "MetaPlaceTypesGet200ApplicationXmlResponse": "PlaceCategoryArray",
        "MetaPlaceTypesGet200TextXmlResponse": "PlaceCategoryArray",
        "Type-types-Get200ApplicationJsonResponse": "PlaceArray",
        "Type-types-Get200TextJsonResponse": "PlaceArray",
        "Type-types-Get200ApplicationXmlResponse": "PlaceArray",
        "Type-types-Get200TextXmlResponse": "PlaceArray",
        "id-Get200ApplicationJsonResponse": "PlaceArray",
        "id-Get200TextJsonResponse": "PlaceArray",
        "id-Get200ApplicationXmlResponse": "PlaceArray",
        "id-Get200TextXmlResponse": "PlaceArray",
        "Get200ApplicationJsonResponse-1": "StopPointArray",
        "Get200TextJsonResponse": "StopPointArray",
        "Get200ApplicationXmlResponse": "StopPointArray",
        "Get200TextXmlResponse": "StopPointArray",
        "SearchGet200ApplicationJsonResponse": "PlaceArray",
        "SearchGet200TextJsonResponse": "PlaceArray",
        "SearchGet200ApplicationXmlResponse": "PlaceArray",
        "SearchGet200TextXmlResponse": "PlaceArray",
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
        "ids-ArrivalsGet200ApplicationJsonResponse": "PredictionArray",
        "ids-ArrivalsGet200TextJsonResponse": "PredictionArray",
        "ids-ArrivalsGet200ApplicationXmlResponse": "PredictionArray",
        "ids-ArrivalsGet200TextXmlResponse": "PredictionArray",
    },
    "crowding": {},
    "occupancy": {
        "Tfl": "Tfl.Api.Presentation.Entities.Bay",
        "Tfl-2": "Tfl.Api.Presentation.Entities.CarParkOccupancy",
        "Tfl-3": "Tfl.Api.Presentation.Entities.ChargeConnectorOccupancy",
        "Tfl-4": "Tfl.Api.Presentation.Entities.BikePointOccupancy",
    },
}
