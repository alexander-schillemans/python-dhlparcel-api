from typing import Type
from typing_extensions import Literal

from http import HTTPStatus
import datetime
import json

from .cache_handler import CacheHandler
from . import config

class AuthHandler:

    def __init__(self, api: object, user_id: str, key: str = None) -> None:
        self.user_id = user_id
        self.key = key
        
        self._api = api
        self._cache_handler = CacheHandler(fail_silently=True)
        self._auth_token = None
        self._auth_token_exp = None
        self._refresh_token = None
        self._refresh_token_exp = None
    
    def authenticate(self) -> dict:
        """ Tries to authenticate to DHL Parcel. Returns the auth_tokens as dict. It has the following flow:
        1. Check if there are tokens in cache, if so, use them. If not, get new auth tokens by using user_id and key.
        2. If there are tokens in cache, check if the access token has expired;
        3. If the access token is expired, but the refresh token is still valid: retrieve new token by refresh token;
        4. If the access token is not expired; use this token;
        4. else, retrieve new auth tokens using user_id and key."""
        
        auth_tokens = self._cache_handler.get(self.user_id)
        
        if auth_tokens:
            self._set_auth_tokens(auth_tokens)
            
            if self._is_token_expired('access') and not self._is_token_expired('refresh'):
                self._get_auth_tokens_from_refresh_token()
            else:
                self._get_auth_tokens()
        else:
            auth_tokens = self._get_auth_tokens()
        
        return auth_tokens
            
    
    def _get_auth_tokens(self) -> dict:
        """ Retrieves the access and refresh tokens for a given user_id and key. """
        response = self._api._do_request('POST', config.AUTH_URL, { 'userId' : self.user_id, 'key' : self.key }, prepend_base_to_url = False)
        resp_content = self.decode_json_or_none(response.content)
        status = response.status_code
        
        if status == HTTPStatus.UNAUTHORIZED: raise ValueError('The request received a status 401 UNAUTHORIZED. Do you have the correct user_id and key set?')
        if not resp_content: raise ValueError('The request did not return valid JSON.')
        if status != HTTPStatus.OK: raise ValueError('An error occured during authentication: ' + json.dumps(resp_content))
        self._set_auth_tokens(resp_content)
        
        return resp_content
    
    def _get_auth_tokens_from_refresh_token(self) -> dict:
        """ Tries to retrieve new tokens from the refresh token. """
        
        if not self._refresh_token: raise ValueError('No refresh token found. Init the auth flow manually.')
        if self._is_token_expired('refresh'): raise ValueError('Refresh token has expired. Init the auth flow manually.')
        
        response = self._api._do_request('POST', config.REFRESH_TOKEN_URL, { 'refreshToken' : self._refresh_token }, prepend_base_to_url = False)
        resp_content = self.decode_json_or_none(response.content)
        status = response.status_code
        
        if status == HTTPStatus.UNAUTHORIZED: raise ValueError('The request received a status 401 UNAUTHORIZED. Do you have the correct user_id and key set?')
        if not resp_content: raise ValueError('The request did not return valid JSON.')
        if status != HTTPStatus.OK: raise ValueError('An error occured during authentication: ' + json.dumps(resp_content))
        self._set_auth_tokens(resp_content)
        
        return resp_content
    
    def _is_token_expired(self, type: Literal['access', 'refresh'] = 'access') -> bool:
        """ Checks if the access OR request token has expired. Returns True if expired, False if not.
        Type: either 'access' or 'refresh', given the token you want to check. Default is 'access'.
        """
        
        if type == 'access':
            if not self._auth_token_exp: raise ValueError('"auth_token_exp" is empty. Did you retrieve the auth tokens first?')
            token_exp_timestamp = self._auth_token_exp
        elif type == 'refresh':
            if not self._refresh_token_exp: raise ValueError('"refresh_token_exp" is empty. Did you retrieve the auth tokens first?')
            token_exp_timestamp = self._refresh_token_exp
        
        today = datetime.datetime.today()
        expires_at = datetime.datetime.fromtimestamp(token_exp_timestamp)
        
        return True if today > expires_at else False
    
    def _set_auth_tokens(self, auth_tokens: dict) -> None:
        """ Sets the returned auth tokens and writes it to cache. """
        
        self._cache_handler.write(self.user_id, auth_tokens)

        self._auth_token = auth_tokens.get('accessToken')
        self._auth_token_exp = auth_tokens.get('accessTokenExpiration')
        self._refresh_token = auth_tokens.get('refreshToken')
        self._refresh_token_exp = auth_tokens.get('refreshTokenExpiration')
        
    def decode_json_or_none(self, json_value):
        try:
            json_dict = json.loads(json_value)
            return json_dict
        except ValueError:
            return None