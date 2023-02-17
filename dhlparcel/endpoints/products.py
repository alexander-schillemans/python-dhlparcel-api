from typing import Optional
from typing_extensions import Literal
from http import HTTPStatus

from .base import APIEndpoint
from dhlparcel.models.base import ObjectListModel

class ProductMethods(APIEndpoint):
    
    def __init__(self, api: object) -> None:
        super().__init__(api, 'products')
    
    def list(self,
        businessUnit: Optional[str] = None,
        fromCountry: Optional[str] = None,
        toCountry: Optional[str] = None,
        businessProduct: Optional[bool] = None,
        carrier: Optional[Literal['DHL-PARCEL', 'DHL-EXPRESS', 'SPEEDPACK']] = None
    ) -> ObjectListModel:
        
        """ List all products. """
        
        data = {}
        if businessUnit: data['businessUnit'] = businessUnit
        if fromCountry: data['fromCountry'] = fromCountry
        if toCountry: data['toCountry'] = toCountry
        if businessProduct: data['businessProduct'] = businessProduct
        if carrier: data['carrier'] = carrier
        
        status, headers, resp_json = self.api.get(self.endpoint, data)
        if status != HTTPStatus.OK: return ObjectListModel().set_error(returned_content=resp_json, status=status)
        
        return ObjectListModel().construct_from_response(resp_json)