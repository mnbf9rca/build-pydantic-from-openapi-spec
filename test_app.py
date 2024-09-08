from app import endpoints, models

def test_CrowdingClient_naptan():
    client = endpoints.CrowdingClient()
    response = client.naptan("940GZZLUBND")
    assert isinstance(response.content, models.GenericResponseModel)

def test_Line_MetaModes():
    client = endpoints.LineClient()
    response = client.metamodes()
    assert isinstance(response.content, models.ModeArray)

if __name__ == "__main__":
    test_CrowdingClient_naptan()
    # test_Line_MetaModes()