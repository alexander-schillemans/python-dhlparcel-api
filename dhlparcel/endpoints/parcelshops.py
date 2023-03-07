from typing import Optional, List
from typing_extensions import Literal


from .base import APIEndpoint
from dhlparcel.models.base import ObjectListModel, BaseModel

class ParcelShopMethods(APIEndpoint):
    
    def __init__(self, api: object) -> None:
        super().__init__(api, 'parcel-shop-locations')
    
    def get(self,
        countryCode: str,
        id: str
    ) -> BaseModel:
        
        """ Get a specific parcelshop by country and id. """
        
        url = f'{self.endpoint}/{countryCode}/{id}'
        
        status, headers, resp_json = self.api.get(url)
        if status > 399: return BaseModel().set_error(returned_content=resp_json, status=status)
        
        return BaseModel().construct_from_response(resp_json)
        
    
    def list(self,
        countryCode: str,
        limit: Optional[int] = None,
        longitude: Optional[float] = None,
        latitude: Optional[float] = None,
        radius: Optional[int] = None,
        q: Optional[str] = None,
        fuzzy: Optional[str] = None,
        houseNumber: Optional[str] = None,
        street: Optional[str] = None,
        postalCode: Optional[str] = None,
        city: Optional[str] = None,
        showUnavailable: Optional[bool] = None,
        serviceType: Optional[List[str]] = None,
        isLocker: Optional[bool] = None,
        sameDepot: Optional[bool] = None,
        collectionTime: Optional[bool] = None,
    ) -> ObjectListModel:
        
        """ Get a list of all parcelshops by country. Atleast one of the following filter needs to be used: "fuzzy", "postalCode", "street", "city", "houseNumber". """
        
        if not fuzzy and not postalCode and not street and not city and not houseNumber:
            raise ValueError(' Atleast one of the following filter needs to be used: "fuzzy", "postalCode", "street", "city", "houseNumber"')
        
        url = f'{self.endpoint}/{countryCode}'
        
        data = {}
        if limit: data['limit'] = limit
        if longitude: data['longitude'] = longitude
        if latitude: data['latitude'] = latitude
        if radius: data['radius'] = radius
        if q: data['q'] = q
        if fuzzy: data['fuzzy'] = fuzzy
        if houseNumber: data['houseNumber'] = houseNumber
        if street: data['street'] = street
        if zipCode: data['zipCode'] = zipCode
        if postalCode: data['postalCode'] = postalCode
        if city: data['city'] = city
        if showUnavailable: data['showUnavailable'] = showUnavailable
        if serviceType: data['serviceType'] = serviceType
        if isLocker: data['isLocker'] = isLocker
        if sameDepot: data['sameDepot'] = sameDepot
        if collectionTime: data['collectionTime'] = collectionTime
        
        status, headers, resp_json = self.api.get(url, data)
        if status > 399: return ObjectListModel().set_error(returned_content=resp_json, status=status)
        
        return ObjectListModel().construct_from_response(resp_json)