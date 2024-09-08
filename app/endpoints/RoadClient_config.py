base_url = "https://api.tfl.gov.uk"
endpoints = {
    'Road_Get': {'uri': '/Road/', 'model': 'ArrayOfRoadCorridors'},
    'Road_GetByPathIds': {'uri': '/Road/{0}', 'model': 'ArrayOfRoadCorridors'},
    'Road_StatusByPathIdsQueryStartDateQueryEndDate': {'uri': '/Road/{0}/Status', 'model': 'ArrayOfRoadCorridors'},
    'Road_DisruptionByPathIdsQueryStripContentQuerySeveritiesQueryCategoriesQuery': {'uri': '/Road/{0}/Disruption', 'model': 'ArrayOfRoadDisruptions'},
    'Road_DisruptedStreetsByQueryStartDateQueryEndDate': {'uri': '/Road/all/Street/Disruption', 'model': 'Object'},
    'Road_DisruptionByIdByPathDisruptionIdsQueryStripContent': {'uri': '/Road/all/Disruption/{0}', 'model': 'RoadDisruption'},
    'Road_MetaCategories': {'uri': '/Road/Meta/Categories', 'model': 'ArrayOfStrings'},
    'Road_MetaSeverities': {'uri': '/Road/Meta/Severities', 'model': 'ArrayOfStatusSeverities'},
}
