from http import HTTPStatus

from .base import APIEndpoint
from dhlparcel.models.base import ObjectListModel

class PickupAvailabilityMethods(APIEndpoint):
    
    def __init__(self, api: object) -> None:
        super().__init__(api, 'pickup-availability')
        
    def get(self) -> NotImplementedError:
        raise NotImplementedError('Pickup Availability endpoint does not have a "get" function. Use "list" instead.')
    
    def list(self,
        countryCode: str,
        postalCode: str
    ) -> ObjectListModel:

        """ List all Pickup Availabilities for a given country and postal code. """
        
        data = {
            'countryCode' : countryCode,
            'postalCode' : postalCode
        }
        
        status, headers, resp_json = self.api.get(self.endpoint, data)
        if status != HTTPStatus.OK: return ObjectListModel().set_error(returned_content=resp_json, status=status)
        
        return ObjectListModel().construct_from_response(resp_json)