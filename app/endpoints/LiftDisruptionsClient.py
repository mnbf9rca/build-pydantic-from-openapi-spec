from ..Client import Client
from .LiftDisruptionsClient_config import endpoints
from .. import models
from ..package_models import ApiError

class LiftDisruptionsClient(Client):
    def get(self, ) -> models.ArrayOfLiftDisruptions | ApiError:
        '''
        List of all currently disrupted lift routes

        Parameters:
        No parameters required.
        '''
        return self._send_request_and_deserialize(endpoints['get'], endpoint_args=None)

