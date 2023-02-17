from typing_extensions import Literal
from typing import Optional
from http import HTTPStatus

from .base import APIEndpoint
from dhlparcel.models.base import ObjectListModel

class CapabilityMethods(APIEndpoint):
    
    def __init__(self, api: object) -> None:
        super().__init__(api, 'capabilities')
        
    def get(self,
        senderType: Literal['business', 'consumer', 'parcelShop'],
        fromCountry: str,
        toCountry: str,
        toBusiness: bool,
        returnProduct: Optional[bool] = None,
        parcelType: Optional[str] = None,
        option: Optional[list] = None,
        fromPostalCode: Optional[str] = None,
        toPostalCode: Optional[str] = None,
        toCity: Optional[str] = None,
        accountNumber: Optional[str] = None,
        organisationId: Optional[str] = None,
        businessUnit: Optional[str] = None,
        carrier: Optional[Literal['DHL-PARCEL', 'DHL-EXPRESS', 'SPEEDPACK']] = None,
        referenceTimeStamp: Optional[str] = None,
        quantity: Optional[int] = None
    ) -> ObjectListModel:

        """ Retrieves all the capabilities for the given sendType, fromCountry, toCountry and toBusiness. """
        
        
        url = f'{self.endpoint}/{senderType}'
        
        data = {
            'fromCountry' : fromCountry,
            'toCountry' : toCountry,
            'toBusiness' : 'true' if toBusiness else 'false'
        }
        
        if returnProduct: data['returnProduct'] = returnProduct
        if parcelType: data['parcelType'] = parcelType
        if option: data['option'] = option
        if fromPostalCode: data['fromPostalCode'] = fromPostalCode
        if toPostalCode: data['toPostalCode'] = toPostalCode
        if toCity: data['toCity'] = toCity
        if accountNumber: data['accountNumber'] = accountNumber
        if organisationId: data['organisationId'] = organisationId
        if businessUnit: data['businessUnit'] = businessUnit
        if carrier: data['carrier'] = carrier
        if referenceTimeStamp: data['referenceTimeStamp'] = referenceTimeStamp
        if quantity: data['quantity'] = quantity
        
        status, headers, resp_json = self.api.get(url, data)
        if status != HTTPStatus.OK: return ObjectListModel().set_error(returned_content=str(resp_json), status=status)
        
        return ObjectListModel().construct_from_response(resp_json)
    