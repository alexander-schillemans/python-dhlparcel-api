from .base import BaseModel

class Error(BaseModel):

    def __init__(self,
        status=None
    ):
        
        self.status = status