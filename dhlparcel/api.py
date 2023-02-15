import requests
import json
from typing import Tuple
from typing_extensions import Literal

from . import config
from .auth_handler import AuthHandler

class DHLParcel_API:

    def __init__(self, user_id: str, key: str) -> None:
        self.user_id = user_id
        self.key = key
        
        self._base_url = config.BASE_URL
        self._headers = { 'Content-Type' : 'application/json', 'Accept' : 'application/json' }
        self._auth_handler = AuthHandler(self, user_id, key)
        self._access_token = None
        
    def _set_token_header(self, token: str) -> None:
        """ Sets the Authorization Bearer token for the next requests. """
        
        self._access_token = token
        self._headers.update({'Authorization' : f'Bearer {token}' })
    
    def _check_header_tokens(self) -> None:
        """ Checks if a token is present in the headers. If not, request one and add to the headers."""
        
        if not self._access_token or not 'Authorization' in self._headers:
            auth_tokens = self._auth_handler.authenticate()
            self._set_token_header(auth_tokens.get('accessToken'))

    def _do_request(self, method: Literal['GET', 'POST', 'PUT'], url: str, data: dict = None, headers: dict = None, prepend_base_to_url: bool = True) -> requests.Response:
        """ Makes a request to the given url, with the given method and data; updates headers with new values if given.
        By default, the BASE_URL is prepended to the URL. If the arg "prepend_base_to_url" is set to False, it will not be prepended.
        """
        
        headers = self._headers.copy().update(headers) if headers else self._headers

        if prepend_base_to_url:
            request_url = f'{self._base_url}/{url}'
        else:
            request_url = url
        
        if method == 'GET':
            response = requests.get(request_url, params=data, headers=headers)
        elif method == 'POST':
            response = requests.post(request_url, data=json.dumps(data), headers=headers)
        elif method == 'PUT':
            response = requests.put(request_url, data=json.dumps(data), headers=headers)
        
        return response


    def _request(self, method: Literal['GET', 'POST', 'PUT'], url: str, data: dict = None, headers: dict = None, **kwargs: dict) -> Tuple[int, dict, dict]:
        """ Checks the header tokens and then carries out the request.
        Returns the status code, returned headers and content in JSON format. """
        # Check the headers for appropriate tokens before we make a request
        self._check_header_tokens()

        # Make the request
        response = self._do_request(method, url, data, headers, **kwargs)
        response_type = response.headers.get('Content-Type', '')
        resp_content = response.json() if response_type == 'application/json' else response.content
        
        print(resp_content)
        
        return response.status_code, response.headers, resp_content
    
    def _get(self, url: str, data: dict = None, headers: dict = None, **kwargs: dict) -> Tuple[int, dict, dict]:
        status, headers, response = self._request('GET', url, data, headers, **kwargs)
        return status, headers, response
    
    def _post(self, url: str, data: dict = None, headers: dict = None, **kwargs: dict) -> Tuple[int, dict, dict]:
        status, headers, response = self._request('POST', url, data, headers, **kwargs)
        return status, headers, response
    
    def _put(self, url: str, data: dict = None, headers: dict = None, **kwargs: dict) -> Tuple[int, dict, dict]:
        status, headers, response = self._request('PUT', url, data, headers, **kwargs)
        return status, headers, response