from typing import Optional, Union
from typing_extensions import Literal



from .base import APIEndpoint
from dhlparcel.models.base import ObjectListModel, BaseModel

class LabelMethods(APIEndpoint):
    
    def __init__(self, api: object) -> None:
        super().__init__(api, 'labels')
        
    def get(self,
        id: str,
        data_format: Literal['pdf', 'json'] = 'pdf'
    ) -> Union[BaseModel, bytes]:
        headers = { 'Accept' : 'application/pdf' } if data_format == 'pdf' else {}
        
        """ Get a specific label by id. Get the returned content in json or pdf (bytes). """
        
        url = f'{self.endpoint}/{id}'
        status, headers, resp = self.api.get(url, headers=headers)
        if status > 399: return BaseModel().set_error(returned_content=str(resp), status=status)
        
        if data_format == 'pdf':
            return resp
        elif data_format == 'json':
            return BaseModel().construct_from_response(resp)
    
    def list(self,
        trackerCodeFilter: Optional[str] = None,
        orderReferenceFilter: Optional[str] = None,
        shipmentId: Optional[str] = None
    ) -> ObjectListModel:
        
        """ Lists all labels given by the choosen filter. """
        
        if not trackerCodeFilter and not orderReferenceFilter and not shipmentId:
            raise ValueError('You must use at least one of the following filters: "trackerCodeFilter", "orderReferenceFilter", "shipmentId". ')
        
        status, headers, resp_json = self.api.get(self.endpoint)
        if status > 399: return ObjectListModel().set_error(returned_content=str(resp_json), status=status)
        
        return ObjectListModel().construct_from_response(resp_json)
    
    def create(self) -> DeprecationWarning:
        raise DeprecationWarning('Create on the Label endpoint is deprecated. Use the Shipment endpoint to create a label. See: https://api-gw.dhlparcel.nl/docs/#/Shipments/createShipment')