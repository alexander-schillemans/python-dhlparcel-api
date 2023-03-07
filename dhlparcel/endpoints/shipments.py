from typing import Optional
from typing_extensions import Literal


from .base import APIEndpoint
from dhlparcel.models.base import BaseModel, ObjectListModel

class ShipmentMethods(APIEndpoint):
    
    def __init__(self, api: object) -> None:
        super().__init__(api, 'shipments')
        
    def get_options(self,
        senderType: Literal['business', 'consumer', 'parcelShop'],
        fromCountry: Optional[str] = None,
        toBusiness: Optional[bool] = None,
        carrier: Optional[Literal['DHL-PARCEL', 'DHL-EXPRESS', 'SPEEDPACK']] = None,
        businessUnit: Optional[str] = None,
        whitelistRequired: Optional[bool] = None,
        accountNumber: Optional[str] = None
    ) -> ObjectListModel:
        
        """ Retrieves shipment options. """
        
        url = f'shipment-options/{senderType}'
        
        data = {}
        if carrier: data['carrier'] = carrier
        if fromCountry: data['fromCountry'] = fromCountry
        if businessUnit: data['businessUnit'] = businessUnit
        if whitelistRequired: data['whitelistRequired'] = whitelistRequired
        if accountNumber: data['accountNumber'] = accountNumber
        if toBusiness: data['toBusiness'] = toBusiness
        
        status, headers, resp_json = self.api.get(url, data)
        if status > 399: return ObjectListModel().set_error(returned_content=str(resp_json), status=status)

        return ObjectListModel().construct_from_response(resp_json)

    
    def create(self,
        shipmentId: str,
        pieces: list,
        receiver: dict,
        shipper: dict,
        options: list, 
        accountId: Optional[str] = None,
        orderReference: Optional[str] = None,
        onBehalfOf: Optional[dict] = None,
        product: Optional[str] = None,
        customsDeclaration: Optional[dict] = None,
        returnLabel: Optional[bool] = None
    ) -> BaseModel:
        
        """ Creates a new shipment. """
        
        accountId = accountId if accountId else self.api.accountNumber
    
        data = {
            'shipmentId' : shipmentId,
            'accountId' : accountId,
            'pieces' : pieces,
            'receiver' : receiver,
            'shipper': shipper
        }
        
        if orderReference: data['orderReference'] = orderReference
        if options: data['options'] = options
        if onBehalfOf: data['onBehalfOf'] = onBehalfOf
        if product: data['product'] = product
        if customsDeclaration: data['customsDeclaration'] = customsDeclaration
        if returnLabel: data['returnLabel'] = returnLabel
        
        status, headers, resp_json = self.api.post(self.endpoint, data)
        if status > 399: return BaseModel().set_error(returned_content=str(resp_json), status=status)
        
        return BaseModel().construct_from_response(resp_json)