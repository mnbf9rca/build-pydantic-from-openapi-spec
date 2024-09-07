import json
import os
import logging
import re
import keyword
import builtins
from urllib.parse import urljoin



from enum import Enum
from typing import Dict, Any, Optional, Union, Type, List, Set, get_origin, get_args, Literal, ForwardRef, Tuple
from pydantic import BaseModel, RootModel, create_model, Field
from pydantic.fields import FieldInfo
from datetime import datetime
from collections import defaultdict, deque
from mappings import tfl_mappings

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# Helper functions
def sanitize_name(name: str) -> str:
    """
    Sanitize class names or field names to ensure they are valid Python identifiers.
    1. Replace invalid characters (like hyphens) with underscores.
    2. Extract the portion after the last underscore for more concise names.
    3. Prepend 'Model_' if the name starts with a number or is a Python keyword.
    """
    # Replace invalid characters (like hyphens) with underscores
    sanitized = re.sub(r"[^a-zA-Z0-9_ ]", "_", name).replace(" ", "_")

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

    openapi_type: str = field_spec.get("type", "Any")

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
    return map_openapi_type(openapi_type)


def map_openapi_type(openapi_type: str) -> type | Any:
    return {
        "string": str,
        "integer": int,
        "boolean": bool,
        "number": float,
        "object": dict,
        "array": list,
    }.get(openapi_type, Any)

def create_array_types_from_model_paths(paths: Dict[str, Dict[str, Any]], components: Dict[str, Any]) -> Dict[str, Any]:
    array_types = {}
    for path, methods in paths.items():
        for method, details in methods.items():
            operation_id = details.get("operationId")
            if operation_id:
                response_content = details["responses"]["200"]
                if "content" not in response_content:
                    continue

                response_type = response_content["content"]["application/json"]["schema"].get("type", "")
                if response_type == "array":
                    model_ref = response_content["content"]["application/json"]["schema"]["items"].get("$ref", "")
                    model_name = model_ref.split("/")[-1]
                    if model_name in components:
                        array_model_name = get_array_model_name(model_name)
                        array_types[array_model_name] = create_openapi_array_type(model_ref)
    return array_types

def get_array_model_name(model_name: str) -> str:
    return f"ArrayOf{sanitize_name(model_name)}"

def create_openapi_array_type(model_ref: str) -> Dict[str, Any]:
    return {
        "type": "array",
        "items": {
            "$ref": f"{model_ref}"
        }
    }

# Create Pydantic models
def create_pydantic_models(components: Dict[str, Any], models: Dict[str, Type[BaseModel] | type]) -> None:
    # First pass: create object models
    for model_name, model_spec in components.items():
        sanitized_name = sanitize_name(model_name)  # Ensure the model name is valid
        if model_spec.get("type") == "object":
            if "properties" not in model_spec:
                # Fallback if 'properties' is missing
                # just create a List model which accepts any dict
                models[sanitized_name] = Dict[str, Any]
                logging.warning(f"Object model {sanitized_name} has no valid 'properties'. Using Dict[str, Any].")
                continue
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
def determine_typing_imports(model_fields: dict[str, FieldInfo], models: dict[str, Type[BaseModel] | type], circular_models: set) -> set:
    """Determine necessary typing imports based on the field annotation."""
    import_set = set()
    
    for field in model_fields.values():
        field_annotation = get_type_str(field.annotation, models)
        if "Optional" in field_annotation:
            import_set.add("Optional")
        if "List" in field_annotation:
            import_set.add("List")
        if "Union" in field_annotation:
            import_set.add("Union")
        if field_annotation in circular_models:
            import_set.add("ForwardRef")
        
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

        init_f.write(f"\n__all__ = [\n    {',\n    '.join(f'\"{key}\"' for key in models.keys())}\n]\n")

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
    os.makedirs(models_dir, exist_ok=True)

    with open(model_file, "w") as mf:
        

        if is_list_or_dict_model(model):
            mf.write("from pydantic import RootModel\n")
            handle_list_or_dict_model(mf, model, models, dependency_graph, circular_models, sanitized_model_name)
        else:
            mf.write("from pydantic import BaseModel, Field\n")
            handle_regular_model(mf, model, models, dependency_graph, circular_models, sanitized_model_name)

        init_f.write(f"from .{sanitized_model_name} import {sanitized_model_name}\n")

def get_builtin_types() -> set:
    """Return a set of all built-in Python types."""
    return {obj for name, obj in vars(builtins).items() if isinstance(obj, type)}


def is_list_or_dict_model(model: Any) -> str | None:
    """Determine if the model is a list or dict type and return the type string ('List' or 'Dict')."""
    origin = get_origin(model)
    if origin is list:
        return "List"
    if origin is dict or origin is Dict:
        return "Dict"
    return None

def handle_list_or_dict_model(mf, model, models, dependency_graph, circular_models, sanitized_model_name):
    """Handle models that are either list or dict types."""
    inner_type = model.__args__[0]
    # Check if the model is a List or Dict
    model_type = is_list_or_dict_model(model)
    # Separate sets for typing imports and module imports
    typing_imports = {model_type}
    module_imports = set()

    # Handle non-built-in types for inner_type
    built_in_types = get_builtin_types()
    inner_type_name = getattr(inner_type, "__name__", None)
    
    if inner_type_name and inner_type_name not in {"Optional", "List", "Union"}:
        sanitized_inner_name = sanitize_name(inner_type_name)
        if sanitized_inner_name in dependency_graph:
            module_imports.add(f"from .{sanitized_inner_name} import {sanitized_inner_name}")
        elif inner_type not in built_in_types:
            typing_imports.add(inner_type_name)


    
    # create the class definition
    if model_type == "List":
        class_definition = f"class {sanitized_model_name}(RootModel[List[{inner_type_name}]]):\n"
    elif model_type == "Dict":
        class_definition = f"class {sanitized_model_name}(RootModel[Dict[str, Any]]):\n"
        typing_imports.add("Any")
    else:
        raise ValueError("Model is not a list or dict model.")
    # Write typing imports
    if typing_imports:

        typing_imports = typing_imports - get_builtin_types()
        mf.write(f"from typing import {', '.join(sorted(typing_imports))}\n")
    
    # Write module imports
    if module_imports:
        mf.write("\n".join(sorted(module_imports)) + "\n")

    # Write class definition
    mf.write(f"\n\n{class_definition}")

    mf.write("    class Config:\n")
    mf.write("        from_attributes = True\n\n")


def handle_regular_model(mf, model: BaseModel, models: Dict[str, Any], dependency_graph: Dict[str, set], circular_models: set, sanitized_model_name: str):
    if hasattr(model, "model_fields"):
        # Determine necessary imports for regular models
        typing_imports = determine_typing_imports(model.model_fields, models, circular_models) - get_builtin_types()
        import_set = {f"from typing import {', '.join(typing_imports)}"}
        # TODO check this

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
                        os.makedirs(models_dir, exist_ok=True)
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


def create_mermaid_class_diagram(dependency_graph: Dict[str, Set[str]], sort_order: List, output_file: str):
    with open(output_file, "w") as f:
        f.write("classDiagram\n")
        for model in sort_order:
            for dep in dependency_graph.get(model, []):
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
    return graph, circular_models, sorted_models


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
        api_path = "/" + spec.get("servers", [{}])[0].get("url", "").split('/', 3)[3]
        logging.info(f"Processing {api_name}")
        update_entities(spec, api_name, pydantic_names)
        combined_components.update(spec.get("components", {}).get("schemas", {}))
        these_paths = spec.get("paths", {})
        # add /api_path to the paths
        for path, methods in these_paths.items():
            new_path = urljoin(api_path + '/', path.lstrip('/'))
            combined_paths[new_path] = methods
        # combined_paths.update(spec.get("paths", {}))

    return combined_components, combined_paths


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
                    logging.info(f"Model '{model_name}' is a duplicate of '{dedup_model_name}'")
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
                    logging.info(f"Model '{model_name}' is a duplicate of '{dedup_model_name}'")
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
def join_url_paths(a: str, b: str) -> str:
    # Ensure the base path ends with a slash for urljoin to work properly
    return urljoin(a + '/', b.lstrip('/'))


def create_config(spec: Dict[str, Any], output_path: str, base_url: str) -> None:
    # Extract paths and components from the spec
    class_name = sanitize_name(spec["info"]["title"])
    paths = spec.get("paths", {})
    components = spec.get("components", {}).get("schemas", {})

    # Create the config content
    config_lines = []
    api_path = "/" + spec.get("servers", [{}])[0].get("url", "").split('/', 3)[3]
    config_lines.append(f'base_url = "{base_url}"\n')
    config_lines.append("endpoints = {\n")

    for path, methods in paths.items():
        for method, details in methods.items():
            operation_id = details.get("operationId")
            if operation_id:
                response_content = details["responses"]["200"]
                if "content" not in response_content:
                    continue
                model_name = get_model_name_from_path(details, response_content)
                if not model_name:
                    continue
                # Strip the base_url from the full URL to leave just the path
                path_uri = join_url_paths(api_path, path.replace(base_url, ""))
                config_lines.append(f"    '{operation_id}': {{'uri': '{path_uri}', 'model': '{model_name}'}},\n")

    config_lines.append("}\n")

    # Write the config to the output file
    config_file_path = os.path.join(output_path, "endpoints",  f"{class_name}_config.py")
    os.makedirs(os.path.dirname(config_file_path), exist_ok=True)

    with open(config_file_path, "w") as config_file:
        config_file.writelines(config_lines)

    logging.info(f"Config file generated at: {config_file_path}")

def classify_parameters(parameters: List[Dict[str, Any]]) -> Tuple[List[str], List[str]]:
    """Classify parameters into path and query parameters."""
    path_params = [param['name'] for param in parameters if param['in'] == 'path']
    query_params = [param['name'] for param in parameters if param['in'] == 'query']
    return path_params, query_params

def create_class(spec: Dict[str, Any], output_path: str) -> None:
    paths = spec.get("paths", {})
    class_name = sanitize_name(spec["info"]["title"])
    
    class_lines = []
    class_lines.append("from ..Client import Client\n")
    class_lines.append(f"from .{class_name}_config import endpoints\n")
    class_lines.append("from .. import models\n")
    class_lines.append("from ..package_models import ApiError\n\n")
    path_lines = [f"class {class_name}(Client):\n"]

    all_types = set()
    
    for path, methods in paths.items():
        for method, details in methods.items():
            operation_id = details.get("operationId")
            if operation_id:
                parameters: List[Dict[str, Any]] = details.get("parameters", [])
                all_types.update([map_openapi_type(param["schema"]["type"]) for param in parameters])
                
                param_str = create_function_parameters(parameters)
                response_content = details["responses"]["200"]
                if "content" not in response_content:
                    continue
                model_name = get_model_name_from_path(details, response_content)
                if not model_name:
                    continue

                # Classify parameters into path and query
                path_params, query_params = classify_parameters(parameters)
                
                # Add function definition
                path_lines.append(f"    def {operation_id.lower()}(self, {param_str}) -> models.{model_name} | ApiError:\n")

                # Add docstring
                docstring = details.get("description", "No description available.")
                if parameters:
                    docstring_parameters = "\n".join([f"        {param['name']}: {map_openapi_type(param['schema']['type']).__name__} - {param.get('description', '')}. Example: {param.get('example', 'None given')}" for param in parameters])
                else:
                    docstring_parameters = "        No parameters required."
                path_lines.append(f"        '''\n        {docstring}\n\n        Parameters:\n{docstring_parameters}\n        '''\n")

                # Generate the call to `_send_request_and_deserialize`
                formatted_path_params = ", ".join(path_params)
                formatted_query_params = ", ".join([f"'{param}': {param}" for param in query_params])
                
                if formatted_query_params:
                    query_params_dict = f"endpoint_args={{ {formatted_query_params} }}"
                else:
                    query_params_dict = "endpoint_args=None"
                
                if path_params:
                    path_lines.append(f"        return self._send_request_and_deserialize(endpoints['{operation_id}'], params=[{formatted_path_params}], {query_params_dict})\n\n")
                else:
                    path_lines.append(f"        return self._send_request_and_deserialize(endpoints['{operation_id}'], {query_params_dict})\n\n")

    # Import types from typing
    valid_type_imports = all_types - get_builtin_types()
    valid_type_import_strings = [t.__name__ for t in valid_type_imports]
    if valid_type_import_strings:
        class_lines.append(f"from typing import {', '.join(valid_type_import_strings)}\n\n")
    
    # Write the class to the output file
    class_file_path = os.path.join(output_path, "endpoints", f"{class_name}.py")
    os.makedirs(os.path.dirname(class_file_path), exist_ok=True)
    with open(class_file_path, "w") as class_file:
        class_file.writelines(class_lines)
        class_file.writelines(path_lines)

    logging.info(f"Class file generated at: {class_file_path}")

def get_model_name_from_path(details, response_content, only_arrays: bool = False) -> str:
    response_type = response_content["content"]["application/json"]["schema"].get("type", "")
    if response_type == "array":
        model_ref = response_content["content"]["application/json"]["schema"]["items"].get("$ref", "")
        return get_array_model_name(sanitize_name(model_ref.split("/")[-1])) if model_ref else ""
    elif not only_arrays:
        model_ref = details["responses"]["200"]["content"]["application/json"]["schema"].get("$ref", "")
        return model_ref.split("/")[-1] if model_ref else ""


def create_function_parameters(parameters: List[Dict[str, Any]]) -> str:
    # Sort parameters to ensure required ones come first
    sorted_parameters = sorted(parameters, key=lambda param: not param.get("required", False))
    
    param_str = ", ".join(
        [
            f"{param['name']}: {map_openapi_type(param['schema']['type']).__name__} | None = None"
            if not param.get("required", False)
            else f"{param['name']}: {map_openapi_type(param['schema']['type']).__name__}"
            for param in sorted_parameters
        ]
    )
    return param_str

def save_classes(specs: List[Dict[str, Any]], base_path: str, base_url: str) -> None:
    """Create config and class files for each spec in the specs list."""
    init_file_path = os.path.join(base_path, "__init__.py")
    with open(init_file_path, "w") as init_file:
        init_file.write("\n".join([f"from .endpoints.{sanitize_name(get_api_name(spec))} import {sanitize_name(get_api_name(spec))}" for spec in specs]))
        init_file.write("\nfrom .rest_client import RestClient\n")
        init_file.write("from .package_models import ApiError, ResponseModel\n")
        init_file.write("__all__ = [\n")
        init_file.write(",\n".join([f"    '{sanitize_name(get_api_name(spec))}'" for spec in specs]))
        init_file.write(",\n    'RestClient',\n    'ApiError',\n    'ResponseModel'\n]\n")
        
    for spec in specs:
        api_name = get_api_name(spec)
        logging.info(f"Creating config and class files for {api_name}...")

        # Create config and class for each spec
        create_config(spec, base_path, base_url)
        create_class(spec, base_path)

    logging.info("All classes and configs saved.")



# Main function
def main(spec_path: str, output_path: str):
    os.makedirs(output_path, exist_ok=True)
    logging.info("Loading OpenAPI specs...")
    specs = load_specs(spec_path)

    logging.info("Generating components...")
    pydantic_names = {}
    combined_components, combined_paths = combine_components_and_paths(specs, pydantic_names)

    logging.info("Creating array types from model paths...")
    # some paths have an array type as a response, we need to handle these separately
    array_types = create_array_types_from_model_paths(combined_paths, combined_components)
    combined_components.update(array_types)

    logging.info("Generating Pydantic models...")
    models = {}
    create_pydantic_models(combined_components, models)

    # Deduplicate models before saving them
    logging.info("Deduplicating models...")
    deduplicated_models, reference_map = deduplicate_models(models)

    # Update model references
    models = update_model_references(deduplicated_models, reference_map)

    logging.info("Handling dependencies...")
    dependency_graph, circular_models, sorted_models = handle_dependencies(models)

    # Now save the deduplicated models
    logging.info("Saving models to files...")
    save_models(deduplicated_models, output_path, dependency_graph, circular_models)

    # Create config and class
    logging.info("Creating config and class files...")
    base_url = "https://api.tfl.gov.uk"
    save_classes(specs, output_path, base_url)
    
    logging.info("Creating Mermaid class diagram...")
    create_mermaid_class_diagram(dependency_graph, sorted_models, os.path.join(output_path, "class_diagram.mmd"))

    logging.info("Processing complete.")


if __name__ == "__main__":
    main("OpenAPI_specs/", "app/")
