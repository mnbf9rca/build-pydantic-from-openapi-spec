base_url = "https://api.tfl.gov.uk"
endpoints = {
    'Mode_GetActiveServiceTypes': {'uri': '/Mode/ActiveServiceTypes', 'model': 'ArrayOfActiveServiceTypes'},
    'Mode_Arrivals': {'uri': '/Mode/{0}/Arrivals', 'model': 'PredictionArray'},
}
