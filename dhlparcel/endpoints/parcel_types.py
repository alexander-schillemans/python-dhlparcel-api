from typing import Optional, List
from typing_extensions import Literal

from http import HTTPStatus

from .base import APIEndpoint
from dhlparcel.models.base import ObjectListModel, BaseModel

class ParcelTypeMethods(APIEndpoint):
    
    def __init__(self, api: object) -> None:
        super().__init__(api, 'parcel-types')
    
    def list(self,
        senderType: Literal['business', 'consumer', 'parcelShop'],
        fromCountry: str,
        toCountry: Optional[str] = None,
        toBusiness: Optional[bool] = None,
        businessUnit: Optional[str] = None,
        fromPostalCode: Optional[str] = None,
        toPostalCode: Optional[str] = None,
        returnProduct: Optional[bool] = None,
        carrier: Optional[List[Literal['DHL-PARCEL', 'DHL-EXPRESS', 'SPEEDPACK']]] = None,
        accountNumber: Optional[str] = None
    ) -> ObjectListModel:
        
        """ Lists all parcel types given by the choosen filter. """
        
        url = f'{self.endpoint}/{senderType}/{fromCountry}'
        
        data = {}
        if toCountry: data['toCountry'] = toCountry
        if businessUnit: data['businessUnit'] = businessUnit
        if fromPostalCode: data['fromPostalCode'] = fromPostalCode
        if toPostalCode: data['toPostalCode'] = toPostalCode
        if toBusiness: data['toBusiness'] = toBusiness
        if returnProduct: data['returnProduct'] = returnProduct
        if carrier: data['carrier'] = carrier
        if accountNumber: data['toCountry'] = accountNumber

        status, headers, resp_json = self.api.get(url)
        if status != HTTPStatus.OK: return ObjectListModel().set_error(returned_content=str(resp_json), status=status)
        
        return ObjectListModel().construct_from_response(resp_json)