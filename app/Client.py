from .rest_client import RestClient
from importlib import import_module
from typing import Any, Literal, List, Optional, Tuple
from requests import Response
import pkgutil
from pydantic import BaseModel
from . import models
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime
from .package_models import ResponseModel, ApiError

class Client:
    """Client

    :param str api_token: API token to access TfL unified API
    """

    def __init__(self, api_token: str = None):
        self.client = RestClient(api_token)
        self.models = self._load_models()

    def _load_models(self):
        models_dict = {}
        for importer, modname, ispkg in pkgutil.iter_modules(models.__path__):
            module = import_module(f".models.{modname}", __package__)
            for model_name in dir(module):
                attr = getattr(module, model_name)
                if isinstance(attr, type) and issubclass(attr, BaseModel):
                    models_dict[model_name] = attr
        # print(models_dict)
        return models_dict

    @staticmethod
    def _parse_int_or_none(value: str) -> int | None:
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _get_maxage_headers_from_cache_control_header(response: Response) -> Tuple[Optional[int], Optional[int]]:
        cache_control = response.headers.get("Cache-Control")
        # e.g. 'public, must-revalidate, max-age=43200, s-maxage=86400'
        if cache_control is None:
            return None, None
        directives = cache_control.split(", ")
        # e.g. ['public', 'must-revalidate', 'max-age=43200', 's-maxage=86400']
        directives = {d.split("=")[0]: d.split("=")[1]
                      for d in directives if "=" in d}
        smaxage = Client._parse_int_or_none(directives.get("s-maxage", ""))
        maxage = Client._parse_int_or_none(directives.get("max-age", ""))
        return smaxage, maxage

    @staticmethod
    def _parse_timedelta(value: Optional[int], base_time: Optional[datetime]) -> Optional[datetime]:
        try:
            return base_time + timedelta(seconds=value) if value is not None and base_time is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _get_result_expiry(response: Response) -> Tuple[datetime | None, datetime | None]:
        s_maxage, maxage = Client._get_maxage_headers_from_cache_control_header(
            response)
        request_datetime = parsedate_to_datetime(response.headers.get(
            "Date")) if "Date" in response.headers else None

        s_maxage_expiry = Client._parse_timedelta(s_maxage, request_datetime)
        maxage_expiry = Client._parse_timedelta(maxage, request_datetime)

        return s_maxage_expiry, maxage_expiry

    def _deserialize(self, model_name: str, response: Response) -> Any:
        shared_expiry, result_expiry = self._get_result_expiry(response)
        Model = self._get_model(model_name)
        data = response.json()

        result = self._create_model_instance(
            Model, data, result_expiry, shared_expiry)

        return result

    def _get_model(self, model_name: str) -> BaseModel:
        Model = self.models.get(model_name)
        if Model is None:
            raise ValueError(f"No model found with name {model_name}")
        return Model

    def _create_model_instance(
        self, Model: BaseModel, response_json: Any, result_expiry: Optional[datetime], shared_expiry: Optional[datetime]
    ) -> ResponseModel:
        content = Model(response_json)
        return ResponseModel(content_expires=result_expiry, shared_expires=shared_expiry, content=content)  

    def _deserialize_error(self, response: Response) -> ApiError:
        # if content is json, deserialize it, otherwise manually create an ApiError object
        if response.headers.get("Content-Type") == "application/json":
            return self._deserialize("ApiError", response)
        return ApiError(
            timestampUtc=parsedate_to_datetime(response.headers.get("Date")),
            exceptionType="Unknown",
            httpStatusCode=response.status_code,
            httpStatus=response.reason,
            relativeUri=response.url,
            message=response.text,
        )

    def _send_request_and_deserialize(
        self, endpoint_and_model: dict[str, str],
        params: str | int | List[str | int] = None, endpoint_args: dict = None
    ) -> BaseModel | List[BaseModel] | ApiError:
        if params is None:
            params = []
        if not isinstance(params, list):
            params = [params]

        endpoint = endpoint_and_model["uri"].format(*params)
        model_name = endpoint_and_model["model"]

        response = self.client.send_request(endpoint, endpoint_args)

        if response.status_code != 200:
            return self._deserialize_error(response)
        return self._deserialize(model_name, response)
