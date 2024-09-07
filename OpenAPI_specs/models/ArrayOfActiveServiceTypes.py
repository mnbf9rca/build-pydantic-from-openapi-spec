from pydantic import RootModel
from .ActiveServiceType import ActiveServiceType
from typing import List


class ArrayOfActiveServiceTypes(RootModel[List[ActiveServiceType]]):

    class Config:
        from_attributes = True
