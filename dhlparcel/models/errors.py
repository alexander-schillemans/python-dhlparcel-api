from .base import BaseModel

class Error(BaseModel):

    def __init__(self,
        status=None,
        returned_content=None
    ):
        
        self.status = status
        self.returned_content = returned_content