class BaseModel:

    def __init__(self):

        self.has_error = False
        self.error = None

    def parse(self, json):
        for key, value in json.items():
            attr_val = getattr(self, key)

            if isinstance(attr_val, BaseModel):
                setattr(self, key, attr_val.parse(value))
            else:
                setattr(self, key, value)

        return self
    
    def get_json(self):

        dikt = {}
        for k, v in self.__dict__.items():
            if v:
                if isinstance(v, BaseModel):
                    json = v.get_json()
                    if json: dikt[k] = json
                else:
                    dikt[k] = v

        return dikt if len(dikt) > 0 else None
    
    def set_error(self, status):
        from .errors import Error
        self.has_error = True
        self.error = Error(status=status)
        
        return self


class ObjectListModel(BaseModel):

    def __init__(self, list=[], list_object=None):
        super().__init__()

        self.list = list
        self.list_object = list_object
        self.has_error = False
        self.error = None

    def add(self, item):
        self.list.append(item)
        return self.list
    
    def remove(self, item):
        self.list.remove(item)
        return self.list
    
    def parse(self, json):

        if isinstance(json, dict):
            itemObj = self.list_object().parse(json)
            self.add(itemObj)
        elif isinstance(json, list):
            for item in json:
                itemObj = self.list_object().parse(item)
                self.add(itemObj)

        return self
    
    def get_json(self):
        list = []

        for item in self.list:
            list.append(item.get_json())
        
        return list if len(list) > 0 else None

    def items(self):
        return self.list