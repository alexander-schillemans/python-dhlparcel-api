from dhlparcel.models.base import BaseModel



class APIEndpoint:

    def __init__(self, api: object, endpoint: str) -> None:

        self.api = api
        self.endpoint = endpoint
        
    def get(self,
        id: str
    ) -> BaseModel:
        
        url = f'{self.endpoint}/{id}'
        status, headers, resp_json = self.api.get(url)
        if status > 399: return BaseModel().set_error(returned_content=str(resp_json), status=status)
        
        return BaseModel().construct_from_response(resp_json)
    
    def list(self):
        raise NotImplementedError('List is not implemented for this endpoint.')
    
    def create(self):
        raise NotImplementedError('Create is not implemented for this endpoint.')
    