import requests
import json
from typing import Tuple, Optional
from typing_extensions import Literal

from . import config
from .auth_handler import AuthHandler

from .endpoints.capabilities import CapabilityMethods
from .endpoints.shipments import ShipmentMethods
from .endpoints.labels import LabelMethods
from .endpoints.parcel_types import ParcelTypeMethods
from .endpoints.products import ProductMethods
from .endpoints.pickup_availability import PickupAvailabilityMethods
from .endpoints.parcelshops import ParcelShopMethods

class DHLParcel_API:

    def __init__(self, user_id: str, key: str, accountNumber: str) -> None:
        self.user_id = user_id
        self.key = key
        self.accountNumber = accountNumber
        
        self._base_url = config.BASE_URL
        self._headers = { 'Content-Type' : 'application/json', 'Accept' : 'application/json' }
        self._auth_handler = AuthHandler(self, user_id, key)
        self._access_token = None
        
        self.capabilities = CapabilityMethods(self)
        self.shipments = ShipmentMethods(self)
        self.labels = LabelMethods(self)
        self.parcel_types = ParcelTypeMethods(self)
        self.products = ProductMethods(self)
        self.pickup_availability = PickupAvailabilityMethods(self)
        self.parcelshops = ParcelShopMethods(self)
        
    def _set_token_header(self, token: str) -> None:
        """ Sets the Authorization Bearer token for the next requests. """
        
        self._access_token = token
        self._headers.update({'Authorization' : f'Bearer {token}' })
    
    def _check_header_tokens(self) -> None:
        """ Checks if a token is present in the headers. If not, request one and add to the headers."""
        
        if not self._access_token or not 'Authorization' in self._headers:
            auth_tokens = self._auth_handler.authenticate()
            self._set_token_header(auth_tokens.get('accessToken'))

    def _prepare_data_for_request(self, data: dict) -> dict:
        """ Gets data to be sent in a request and converts them to the way the DHL API expects. """
        if not data: return None
        
        for key, value in data.items():
            if type(value) == bool:
                data[key] = 'true' if value else 'false' # bool variables need to be converted to strings
        
        return data

    def _update_headers(self, headers: dict) -> dict:
        """ Takes the initial headers and updates it with the given headers. Returns the updated headers. """
        
        tmp_headers = self._headers.copy()
        tmp_headers.update(headers)
        return tmp_headers

    def _do_request(self, method: Literal['GET', 'POST', 'PUT'], url: str, data: Optional[dict] = None, headers: Optional[dict] = None, prepend_base_to_url: Optional[bool] = True) -> requests.Response:
        """ Makes a request to the given url, with the given method and data; updates headers with new values if given.
        By default, the BASE_URL is prepended to the URL. If the arg "prepend_base_to_url" is set to False, it will not be prepended.
        """
        
        headers = self._update_headers(headers) if headers else self._headers

        if prepend_base_to_url:
            request_url = f'{self._base_url}/{url}'
        else:
            request_url = url
        
        data = self._prepare_data_for_request(data)
        
        if method == 'GET':
            response = requests.get(request_url, params=data, headers=headers)
        elif method == 'POST':
            response = requests.post(request_url, data=json.dumps(data), headers=headers)
        elif method == 'PUT':
            response = requests.put(request_url, data=json.dumps(data), headers=headers)
        
        return response


    def _request(self, method: Literal['GET', 'POST', 'PUT'], url: str, data: Optional[dict] = None, headers: Optional[dict] = None, **kwargs: dict) -> Tuple[int, dict, dict]:
        """ Checks the header tokens and then carries out the request.
        Returns the status code, returned headers and content in JSON format. """
        # Check the headers for appropriate tokens before we make a request
        self._check_header_tokens()

        # Make the request
        response = self._do_request(method, url, data, headers, **kwargs)
        response_type = response.headers.get('Content-Type', '')
        resp_content = response.json() if response_type == 'application/json' else response.content

        return response.status_code, response.headers, resp_content
    
    def get(self, url: str, data: Optional[dict] = None, headers: Optional[dict] = None, **kwargs: dict) -> Tuple[int, dict, dict]:
        status, headers, response = self._request('GET', url, data, headers, **kwargs)
        return status, headers, response
    
    def post(self, url: str, data: Optional[dict] = None, headers: Optional[dict] = None, **kwargs: dict) -> Tuple[int, dict, dict]:
        status, headers, response = self._request('POST', url, data, headers, **kwargs)
        return status, headers, response
    
    def put(self, url: str, data: Optional[dict] = None, headers: Optional[dict] = None, **kwargs: dict) -> Tuple[int, dict, dict]:
        status, headers, response = self._request('PUT', url, data, headers, **kwargs)
        return status, headers, response