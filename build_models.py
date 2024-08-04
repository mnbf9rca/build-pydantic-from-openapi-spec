import json
import os
import logging
import re
import keyword
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
        "Tfl-Api-Presentation-Entities-PlaceArray": "Tfl-Api-Presentation-Entities-PlaceArray",
        "Tfl-Api-Presentation-Entities-PlaceArray-1": "Tfl-Api-Presentation-Entities-PlaceArray-1",
        "Tfl-Api-Presentation-Entities-PlaceArray-2": "Tfl-Api-Presentation-Entities-PlaceArray-2",
        "Tfl-Api-Presentation-Entities-PlaceArray-3": "Tfl-Api-Presentation-Entities-PlaceArray-3",
        "Tfl-Api-Presentation-Entities-PlaceArray-4": "Tfl-Api-Presentation-Entities-PlaceArray-4",
        "Tfl-Api-Presentation-Entities-PlaceArray-5": "Tfl-Api-Presentation-Entities-PlaceArray-5",
        "Tfl-Api-Presentation-Entities-PlaceArray-6": "Tfl-Api-Presentation-Entities-PlaceArray-6",
        "Tfl-Api-Presentation-Entities-PlaceArray-7": "Tfl-Api-Presentation-Entities-PlaceArray-7",
        "Tfl.Api.Presentation.Entities.AdditionalProperties": "Tfl.Api.Presentation.Entities.AdditionalProperties",
        "Tfl.Api.Presentation.Entities.Place": "Tfl.Api.Presentation.Entities.Place",
    },
    "Disruptions-Lifts-v2": {"LiftDisruption": "LiftDisruption"},
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
    },
    "Line": {
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
        "Tfl-Api-Presentation-Entities-ActiveServiceTypeArray": "Tfl-Api-Presentation-Entities-ActiveServiceTypeArray",
        "Tfl-Api-Presentation-Entities-ActiveServiceTypeArray-1": "Tfl-Api-Presentation-Entities-ActiveServiceTypeArray-1",
        "Tfl-Api-Presentation-Entities-ActiveServiceTypeArray-2": "Tfl-Api-Presentation-Entities-ActiveServiceTypeArray-2",
        "Tfl-Api-Presentation-Entities-ActiveServiceTypeArray-3": "Tfl-Api-Presentation-Entities-ActiveServiceTypeArray-3",
        "Tfl-Api-Presentation-Entities-PredictionArray-4": "Tfl-Api-Presentation-Entities-PredictionArray-4",
        "Tfl-Api-Presentation-Entities-PredictionArray-5": "Tfl-Api-Presentation-Entities-PredictionArray-5",
        "Tfl-Api-Presentation-Entities-PredictionArray-6": "Tfl-Api-Presentation-Entities-PredictionArray-6",
        "Tfl-Api-Presentation-Entities-PredictionArray-7": "Tfl-Api-Presentation-Entities-PredictionArray-7",
        "Tfl.Api.Presentation.Entities.ActiveServiceType": "Tfl.Api.Presentation.Entities.ActiveServiceType",
        "Tfl.Api.Presentation.Entities.Prediction": "Tfl.Api.Presentation.Entities.Prediction",
        "Tfl.Api.Presentation.Entities.PredictionTiming": "Tfl.Api.Presentation.Entities.PredictionTiming",
    },
    "Place": {
        "System": "System.Object",
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
    },
    "Search": {
        "Tfl": "Tfl.Api.Presentation.Entities.SearchMatch",
        "Tfl-2": "Tfl.Api.Presentation.Entities.SearchResponse",
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
    },
    "crowding": {},
    "occupancy": {
        "Tfl": "Tfl.Api.Presentation.Entities.Bay",
        "Tfl-2": "Tfl.Api.Presentation.Entities.CarParkOccupancy",
        "Tfl-3": "Tfl.Api.Presentation.Entities.ChargeConnectorOccupancy",
        "Tfl-4": "Tfl.Api.Presentation.Entities.BikePointOccupancy",
    },
}


# Function to load all OpenAPI specifications from the specified folder
def load_openapi_specs(folder_path: str) -> List[Dict[str, Any]]:
    specs = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            with open(os.path.join(folder_path, file_name), "r") as file:
                specs.append(json.load(file))
                logging.info(f"Loaded {file_name}")
    return specs


def get_api_name(spec: Dict[str, Any]) -> str:
    return spec["info"]["title"]


def rename_entities_and_update_references(spec: Dict[str, Any], api_name: str, pydantic_names: Dict[str, str]) -> None:
    if api_name not in tfl_mappings:
        return

    entity_mapping = tfl_mappings[api_name]
    components = spec.get("components", {}).get("schemas", {})

    # Rename entities
    for old_name, new_name in entity_mapping.items():
        if old_name in components:
            components[new_name] = components.pop(old_name)
            pydantic_names[old_name] = sanitize_class_name(new_name.split(".")[-1])

    # Recursively update references
    update_references_recursive(spec, entity_mapping)


def update_references_recursive(obj: Any, entity_mapping: Dict[str, str]):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "$ref" and isinstance(value, str):
                ref_name = value.split("/")[-1]
                if ref_name in entity_mapping:
                    new_name = entity_mapping[ref_name]
                    obj[key] = value.replace(ref_name, new_name)
                    logging.info(f"Updated reference: {value} -> {obj[key]}")
            else:
                update_references_recursive(value, entity_mapping)
    elif isinstance(obj, list):
        for item in obj:
            update_references_recursive(item, entity_mapping)


# Function to sanitize class names by replacing hyphens and spaces with underscores
def sanitize_class_name(name: str) -> str:
    return name.replace("-", "_").replace(" ", "_")


# Function to map OpenAPI types to Python types
def map_openapi_type(
    field_spec: Dict[str, Any],
    components: Dict[str, Any],
    models: Dict[str, Type[BaseModel]],
) -> Any:
    if "$ref" in field_spec:
        ref = field_spec["$ref"]
        ref_name = ref.split("/")[-1]
        sanitized_ref_name = sanitize_class_name(ref_name.split(".")[-1])
        if sanitized_ref_name in models:
            logging.info(f"Reusing existing model: {sanitized_ref_name}")
            return models[sanitized_ref_name]
        logging.info(f"Forward reference found: {ref_name}")
        return sanitized_ref_name  # Return the class name as a forward reference

    openapi_type = field_spec.get("type", "Any")
    openapi_format = field_spec.get("format", None)

    if "enum" in field_spec:
        enum_values = tuple(field_spec["enum"])
        return Literal[enum_values]  # noqa: F821

    type_mapping = {
        "string": {None: str, "date-time": datetime},
        "integer": {
            None: int,
            "int32": int,
            "int64": int,  # Python's int can handle 64-bit integers
        },
        "number": {None: float, "double": float},
        "boolean": {None: bool},
        "array": {None: lambda: List[map_openapi_type(field_spec["items"], components, models)]},
        "object": {None: dict},
    }

    return type_mapping.get(openapi_type, {}).get(openapi_format, Any)


# Function to identify and remove duplicate schemas, retaining the preferred names, and update references accordingly
def remove_duplicate_schemas(components: Dict[str, Any]) -> (Dict[str, Any], Dict[str, str]):
    resolved = {}
    ref_map = {}
    schema_to_name = {}

    def process_schema(name: str, schema: Dict[str, Any]):
        schema_key = json.dumps(schema, sort_keys=True)
        if schema_key in schema_to_name:
            preferred_name = schema_to_name[schema_key]
            original_preferred_name = preferred_name
            if name.startswith("Tfl.") or len(name) > 6:
                ref_map[preferred_name] = name
                preferred_name = name
            ref_map[name] = preferred_name
            logging.info(f"Duplicate schema found: {name} -> {original_preferred_name} (using {preferred_name})")

            # Update resolved dictionary to replace the old schema with the preferred one
            resolved[preferred_name] = schema
            if original_preferred_name in resolved:
                del resolved[original_preferred_name]
        else:
            schema_to_name[schema_key] = name
            resolved[name] = schema

    for name, schema in components.items():
        process_schema(name, schema)

    final_ref_map = {k: ref_map.get(v, v) for k, v in ref_map.items()}

    # Update references in all components
    resolved = update_references([{"components": {"schemas": resolved}}], final_ref_map)[0]["components"]["schemas"]

    return resolved, final_ref_map


# Function to update references in the specifications to point to the retained schemas
def update_references(specs: List[Dict[str, Any]], ref_map: Dict[str, str]) -> List[Dict[str, Any]]:
    for spec in specs:
        update_references_recursive(spec, ref_map)
    return specs


# Function to generate Pydantic models from OpenAPI components
def generate_pydantic_models(components: Dict[str, Any], models: Dict[str, Type[BaseModel]]) -> None:
    component_model_mapping = {}

    for model_name, model_spec in components.items():
        sanitized_model_name = sanitize_class_name(model_name.split(".")[-1])
        if model_spec.get("type") == "array":
            fields = {}
            if "items" in model_spec:
                if "$ref" in model_spec["items"]:
                    ref_name = model_spec["items"]["$ref"].split("/")[-1]
                    sanitized_ref_name = sanitize_class_name(ref_name.split(".")[-1])
                    array_model_name = f"ArrayOf{sanitized_ref_name}"
                    component_model_mapping[model_name] = array_model_name
                    if sanitized_ref_name in models:
                        models[array_model_name] = List[models[sanitized_ref_name]]
                        logging.info(f"Created Pydantic model: {array_model_name}")
                    else:
                        models[array_model_name] = List[f'"{sanitized_ref_name}"']
                        logging.info(f"Created Pydantic model with forward reference: {array_model_name}")
                else:
                    array_item_type = map_openapi_type(model_spec["items"], components, models)
                    component_model_mapping[model_name] = sanitized_model_name
                    models[sanitized_model_name] = List[array_item_type]
                    logging.info(f"Created Pydantic model: {sanitized_model_name}")
            # continue  # Skip arrays for now

        elif "properties" in model_spec:
            fields = {}
            required_fields = model_spec.get("required", [])
            for field_name, field_spec in model_spec["properties"].items():
                field_type = map_openapi_type(field_spec, components, models)
                alias = field_name
                if field_name in required_fields:
                    fields[field_name] = (field_type, Field(..., alias=alias))
                else:
                    fields[field_name] = (
                        Optional[field_type],
                        Field(None, alias=alias),
                    )
            if sanitized_model_name in models:
                sanitized_model_name += "_2"
            component_model_mapping[model_name] = sanitized_model_name
            models[sanitized_model_name] = create_model(sanitized_model_name, **fields)
            logging.info(f"Created Pydantic model: {sanitized_model_name}")
    
    return component_model_mapping


# Function to create the configuration dictionary for endpoints
def create_config(
    paths: Dict[str, Any], resolved_components: Dict[str, Any], pydantic_names: Dict[str, str]
) -> Dict[str, Dict[str, str]]:
    config = {}
    for path, path_spec in paths.items():
        for method, method_spec in path_spec.items():
            operation_id = method_spec["operationId"]
            response_schema_ref = method_spec["responses"]["200"]["content"]["application/json"]["schema"]
            model_name = get_model_name_from_schema_ref(response_schema_ref, pydantic_names)
            if (
                model_name in resolved_components
                and resolved_components[model_name]["type"] == "array"
                and "items" in resolved_components[model_name]
                and "$ref" in resolved_components[model_name]["items"]
            ):
                base_model_name = sanitize_class_name(resolved_components[model_name]["items"]["$ref"].split(".")[-1])
                model_name = f"ArrayOf{base_model_name}"
                config[operation_id] = {"uri": path, "model": model_name}
            elif model_name:
                sanitized_model_name = pydantic_names.get(model_name, sanitize_class_name(model_name.split(".")[-1]))
                config[operation_id] = {"uri": path, "model": sanitized_model_name}
    return config


# Helper function to handle forward references and literals
def handle_forward_ref(annotation: Any, forward_refs: Set[str], model_name: str) -> Any:
    if isinstance(annotation, ForwardRef):
        forward_refs.add(model_name)
        return f"{annotation.__forward_arg__}"
    return annotation


def handle_literal(annotation: Any) -> Any:
    if hasattr(annotation, "__origin__") and annotation.__origin__ is Literal:
        literals = ", ".join(repr(v) for v in annotation.__args__)
        return f"Literal[{literals}]"
    return annotation


def get_model_name_from_schema_ref(schema_ref: Dict[str, Any], pydantic_names: Dict[str, str]) -> Optional[str]:
    if "items" in schema_ref and "$ref" in schema_ref["items"]:
        return schema_ref["items"]["$ref"].split("/")[-1]
    elif "$ref" in schema_ref:
        return schema_ref["$ref"].split("/")[-1]
    return None


# Function to determine the field type for a given field annotation
def get_field_type(field_annotation: Any, forward_refs: Set[str], model_name: str) -> str:
    field_annotation = handle_forward_ref(field_annotation, forward_refs, model_name)
    field_annotation = handle_literal(field_annotation)

    if isinstance(field_annotation, str):
        return field_annotation

    origin = get_origin(field_annotation)
    args = get_args(field_annotation)

    if origin is Union and len(args) == 2 and args[1] is type(None):
        inner_type = get_field_type(args[0], forward_refs, model_name)
        return f"Optional[{inner_type}]"
    elif (
        callable(field_annotation)
        and not isinstance(field_annotation, type)
        and not hasattr(field_annotation, "__origin__")
    ):
        evaluated_lambda = field_annotation()
        return get_field_type(evaluated_lambda, forward_refs, model_name)

    if args:
        inner_type = get_field_type(args[0], forward_refs, model_name)
        if origin is list:
            return f"List[{inner_type}]"
        elif origin is dict:
            key_type = get_field_type(args[0], forward_refs, model_name)
            value_type = get_field_type(args[1], forward_refs, model_name)
            return f"Dict[{key_type}, {value_type}]"
        else:
            return f"{origin.__name__}[{inner_type}]"

    if hasattr(field_annotation, "__name__"):
        return field_annotation.__name__
    return "Any"


# Helper function to get the innermost type of a field represented as a string
def get_innermost_type(field_type: str) -> str:
    while field_type.startswith("Optional[") or field_type.startswith("List["):
        field_type = field_type.split("[", 1)[1].rsplit("]", 1)[0]
    return field_type


# Helper function to build the dependency graph
def build_dependency_graph(models: Dict[str, Union[Type[BaseModel], Type[List]]]) -> Dict[str, Set[str]]:
    dependency_graph = defaultdict(set)
    all_models = set(models.keys())

    for model_name, model in models.items():
        if get_origin(model) is list:
            element_type = get_args(model)[0]
            if isinstance(element_type, str):
                dependency_graph[model_name].add(element_type)
            elif hasattr(element_type, "__name__") and element_type.__name__ in all_models:
                dependency_graph[model_name].add(element_type.__name__)
        else:
            for field in model.model_fields.values():
                field_type = get_field_type(field.annotation, set(), model_name)
                innermost_type = get_innermost_type(field_type)
                if innermost_type in all_models:
                    dependency_graph[model_name].add(innermost_type)
        if model_name not in dependency_graph:
            dependency_graph[model_name] = set()

    return dependency_graph


# Function to detect circular dependencies
def detect_circular_dependencies(dependency_graph: Dict[str, Set[str]]) -> Set[str]:
    circular_models = set()
    visited = set()
    stack = set()

    def visit(model: str):
        if model in visited:
            return
        if model in stack:
            circular_models.add(model)
            return
        stack.add(model)
        for dep in dependency_graph[model]:
            visit(dep)
        stack.remove(model)
        visited.add(model)

    for model in dependency_graph:
        visit(model)

    return circular_models


def replace_innermost_type(field_type: Any, new_type: str) -> Any:
    origin = get_origin(field_type)
    args = get_args(field_type)

    if not args:
        return new_type

    if origin is Union and len(args) == 2 and args[1] is type(None):
        inner_type = replace_innermost_type(args[0], new_type)
        return Optional[inner_type]
    elif origin is list:
        inner_type = replace_innermost_type(args[0], new_type)
        return List[inner_type]
    elif origin is dict:
        key_type = replace_innermost_type(args[0], new_type)
        value_type = replace_innermost_type(args[1], new_type)
        return Dict[key_type, value_type]
    else:
        inner_type = replace_innermost_type(args[0], new_type)
        return origin[inner_type]


# Function to modify models to break circular dependencies
def break_circular_dependencies(models: Dict[str, Union[Type[BaseModel], Type[List]]], circular_models: Set[str]):
    for model_name in circular_models:
        model = models[model_name]
        for field_name, field in model.model_fields.items():
            field_annotation = field.annotation
            field_type = get_field_type(field_annotation, set(), model_name)
            innermost_type = get_innermost_type(field_type)
            if innermost_type == model_name:
                new_type = f'"{model_name}"'
                new_field_annotation = replace_innermost_type(field_annotation, new_type)
                models[model_name].model_fields[field_name].annotation = new_field_annotation


# Function to perform topological sorting on the dependency graph
def topological_sort(dependency_graph: Dict[str, Set[str]]) -> List[str]:
    in_degree = {model: 0 for model in dependency_graph}
    for dependencies in dependency_graph.values():
        for dep in dependencies:
            if dep not in in_degree:
                in_degree[dep] = 0
            in_degree[dep] += 1

    queue = deque([model for model in in_degree if in_degree[model] == 0])
    sorted_models = []

    while queue:
        model = queue.popleft()
        sorted_models.append(model)
        for dep in dependency_graph[model]:
            in_degree[dep] -= 1
            if in_degree[dep] == 0:
                queue.append(dep)

    if len(sorted_models) != len(in_degree):
        missing_models = set(in_degree.keys()) - set(sorted_models)
        logging.warning(f"Circular dependencies detected among models: {missing_models}")
        sorted_models.extend(missing_models)

    return sorted_models[::-1]


def sanitize_field_name(field_name: str) -> str:
    if keyword.iskeyword(field_name):
        return f"{field_name}_field"
    return field_name


def camel_to_snake(name: str) -> str:
    """Convert camelCase to snake_case."""
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
    return s2.lower()


# Function to save Pydantic models to a file (updated with topological sorting)
def save_models_to_file(
    models: Dict[str, Union[Type[BaseModel], Type[List]]],
    directory_path: str,
    forward_ref_models: Set[str],
    config: Dict[str, Dict[str, str]],
):
    """Save Pydantic models to separate files and create an __init__.py."""
    output_path = f"{directory_path}/models"
    os.makedirs(f"{output_path}", exist_ok=True)

    dependency_graph = build_dependency_graph(models)
    sorted_models = topological_sort(dependency_graph)

    init_file_path = os.path.join(output_path, "__init__.py")
    with open(init_file_path, "w") as init_file:
        init_file.write("from pydantic import BaseModel, Field\n")
        init_file.write("from typing import Optional, List, Union, ForwardRef, Literal\n")
        init_file.write("from datetime import datetime\n")
        init_file.write("from enum import Enum\n\n")

        imports = []
        all_models = []

        for model_name in sorted_models:
            model_file_path = os.path.join(output_path, f"{model_name}.py")
            with open(model_file_path, "w") as model_file:
                model_file.write(
                    "from pydantic import BaseModel, Field\n"
                    "from typing import Optional, List, Union, ForwardRef, Literal\n"
                    "from datetime import datetime\n"
                    "from enum import Enum\n\n"
                )

                # Write imports for dependencies
                for dependency in dependency_graph[model_name]:
                    model_file.write(f"from {dependency} import {dependency}\n")
                model_file.write("\n")
                model_file.write(f"class {model_name}(BaseModel):\n")
                if get_origin(models[model_name]) is list:
                    array_type = get_field_type(get_args(models[model_name])[0], set(), model_name)
                    if array_type in sorted_models:
                        model_file.write(f"    {array_type}s: List[{array_type}] = Field(None)\n")
                else:
                    for field_name, field in models[model_name].model_fields.items():
                        new_field_name = sanitize_field_name(camel_to_snake(field_name))
                        field_annotation = field.annotation
                        field_type = get_field_type(field_annotation, set(), model_name)
                        if field.default is None:
                            model_file.write(
                                f"    {new_field_name}: {field_type} = Field(None, alias='{field_name}')\n"
                            )
                        else:
                            model_file.write(f"    {new_field_name}: {field_type} = Field(alias='{field_name}')\n")

                # Check if the model is used as a response in the config
                if any(details["model"] == model_name for details in config.values()):
                    model_file.write("    content_expires: Optional[datetime] = Field(None)\n")
                    model_file.write("    shared_expires: Optional[datetime] = Field(None)\n")

                model_file.write('    model_config = {"populate_by_name": True}\n\n')

                if model_name in forward_ref_models:
                    model_file.write(f"{model_name}.model_rebuild()\n")

            imports.append(f"from {model_name} import {model_name}")
            all_models.append(model_name)

        init_file.write("\n".join(imports) + "\n\n")
        init_file.write(f"__all__ = [{',\n    '.join(all_models)}]\n")

    logging.info(f"Models and __init__.py saved to {output_path}")


# Function to save the configuration to a file
def save_config_to_file(config: Dict[str, Dict[str, str]], file_path: str):
    with open(file_path, "w") as file:
        file.write("endpoints = {\n")
        for endpoint, details in config.items():
            file.write(f"    '{endpoint}': {details},\n")
        file.write("}\n")
        logging.info(f"Saved endpoint configuration to {file_path}")


def create_mermaid_class_diagram(dependency_graph: Dict[str, Set[str]], output_file: str):
    """Create a Mermaid class diagram from the dependency graph and write it to a file."""
    with open(output_file, "w") as file:
        file.write("classDiagram\n")
        for model, dependencies in dependency_graph.items():
            for dependency in dependencies:
                file.write(f"    {model} --> {dependency}\n")
    logging.info(f"Mermaid class diagram saved to {output_file}")


# Main function to execute the script
def main(base_path: str):
    logging.info("Loading OpenAPI specifications...")
    specs = load_openapi_specs(base_path)

    logging.info("Combining components from all specifications...")
    pydantic_names = {}
    combined_components, combined_paths = combine_components_and_paths(specs, pydantic_names)

    max_iterations = 200
    resolved_components, updated_paths, ref_map = resolve_duplicate_schemas(
        combined_components, combined_paths, max_iterations, specs
    )

    if not resolved_components:
        logging.error("Max iterations reached. Potential issue with circular references or unresolved schemas.")
        return

    logging.info("Generating Pydantic models...")
    models, component_model_name_mapping = generate_models(resolved_components)

    # rename the keys in resolved_components using the map in component_model_name_mapping
    remapped_resolved_components = {component_model_name_mapping.get(key, key): value for key, value in resolved_components.items()}

    logging.info("Building dependency graph and handling circular dependencies...")
    dependency_graph = handle_dependencies(models)

    logging.info("Creating configuration for endpoints...")
    config = create_config(updated_paths, remapped_resolved_components, pydantic_names)

    logging.info("Saving models and configuration to files...")
    save_output_files(models, base_path, dependency_graph, config)

    logging.info("Processing completed.")


def combine_components_and_paths(
    specs: List[Dict[str, Any]], pydantic_names: Dict[str, str]
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    combined_components = {}
    combined_paths = {}

    for spec in specs:
        api_name = get_api_name(spec)
        logging.info(f"Processing API: {api_name}")
        rename_entities_and_update_references(spec, api_name, pydantic_names)
        combined_components.update(spec.get("components", {}).get("schemas", {}))

        base_path_from_server = get_base_path_from_server(spec)
        update_combined_paths(combined_paths, spec, base_path_from_server)

    return combined_components, combined_paths


def get_base_path_from_server(spec: Dict[str, Any]) -> str:
    if "servers" in spec and isinstance(spec["servers"], list) and len(spec["servers"]) > 0:
        base_url = spec["servers"][0].get("url", "")
        return re.sub(r"https?://[^/]+", "", base_url)
    return ""


def update_combined_paths(combined_paths: Dict[str, Any], spec: Dict[str, Any], base_path_from_server: str):
    for path, path_spec in spec.get("paths", {}).items():
        full_path = base_path_from_server + path
        combined_paths[full_path] = path_spec


def resolve_duplicate_schemas(
    combined_components: Dict[str, Any],
    combined_paths: Dict[str, Any],
    max_iterations: int,
    specs: List[Dict[str, Any]],
) -> Tuple[Dict[str, Any], Dict[str, str]]:
    updated_paths = combined_paths.copy()
    for iteration in range(max_iterations):
        logging.info(f"Iteration {iteration + 1}: Removing duplicate schemas...")
        resolved_components, ref_map = remove_duplicate_schemas(combined_components)

        logging.info("Updating references in all specifications...")
        updated_specs = update_references(specs, ref_map)
        update_references_recursive(updated_paths, ref_map)

        if not ref_map:
            return resolved_components, updated_paths, ref_map

        combined_components = resolved_components

    return None, None


def generate_models(resolved_components: Dict[str, Any]) -> Dict[str, Type[BaseModel]]:
    models = {}
    component_model_name_mapping = generate_pydantic_models(resolved_components, models)
    return models, component_model_name_mapping


def handle_dependencies(models: Dict[str, Type[BaseModel]]) -> Dict[str, Set[str]]:
    logging.info("Building dependency graph...")
    dependency_graph = build_dependency_graph(models)

    logging.info("Detecting circular dependencies...")
    circular_models = detect_circular_dependencies(dependency_graph)

    logging.info("Breaking circular dependencies...")
    break_circular_dependencies(models, circular_models)

    return dependency_graph


def save_output_files(
    models: Dict[str, Type[BaseModel]],
    base_path: str,
    dependency_graph: Dict[str, Set[str]],
    config: Dict[str, Dict[str, str]],
):
    save_models_to_file(models, base_path, dependency_graph, config)
    save_config_to_file(config, f"{base_path}config.py")
    create_mermaid_class_diagram(dependency_graph, f"{base_path}class_diagram.mmd")


base_path = "OpenAPI_specs/"
main(base_path)
