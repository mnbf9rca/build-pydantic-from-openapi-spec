# build-pydantic-from-openapi-spec
my attempt to build Pydantic models from the TfL OpenAPI spec. It automates the creation of around 100 Pydantic models from the TfL OpenAPI spec.

the script reads in the TfL OpenAPI spec (downloaded in JSON format from the [TfL API Portal](https://api-portal.tfl.gov.uk/api-details)) and builds Pydantic models from it. I've created a map for some of the generic types in the TfL OpenAPI spec to Pydantic types.

At the end, it produces a bunch of Pydantic classes (including some enums) that you can use in your code simply by importing the `models` folder. There's also a [mermaid diagram](OpenAPI_specs/class_diagram.mmd) that shows the relationships between the classes.
