# DHL Parcel API
Basic wrapper for the DHL Parcel API (v1).

## Disclaimer
This wrapper does **not** include all API endpoints. I will extend this package as I go and as I need.

This package is in **active development** and is the reason why there is no stable version yet.

## Getting started

### Install
This package is published on PyPi: https://pypi.org/project/python-dhlparcel-api/

Install with pip

```python
pip install python-dhlparcel-api
```

### Import
Import the package and the DHLParcel_API.
```python
from dhlparcel.api import DHLParcel_API
```

### Create connection
You will need your user ID, user key and account number to create a connection.
Find out how you can obtain these here: https://dhlparcel.github.io/api-gtw-docs/#12-services

```python
api = DHLParcel_API(user_id, user_key, account_number)
```

### Authentication
Authentication will happen automatically. 

During a first request, the ```user_id``` and ```user_key``` will be used to obtain an access token and a request token. These tokens will be cached and used for other requests. Once an access token expires, a new one will automatically be retrieved by using the refresh token. If the access token and the refresh token has expired, or are not available inside the cache, the ```user_id``` and ```user_key``` will once again be used to obtain new tokens.

### Retrieving data
You can retrieve data by using the ```.get(id)``` or ```.list()``` functions on a given endpoint. The ```.get()``` function will return a single object and will contain all the returned fields as attributes. The ```.list()``` function will return a list of objects. You can loop over a list by calling ```.items()``` on it.

You can consult the API documentation to know what returned fields to expect.

```python
from dhlparcel.api import DHLParcel_API
api = DHLParcel_API(user_id, user_key, account_number)
parcelshops = api.parcelshops.list('BE', zipCode='2000')

for shop in parcelshops.items():
    print(shop.name)
```

### Creating
Some endpoints allow you to create new objects, such as a label or a shipment.
These endpoints have the ```.create()``` functions available.

Consider the following request needed to create a shipment:

```json
{
  "shipmentId": "15916857-2a31-4238-a45b-e7ba32e0e320",
  "orderReference": "myReference",
  "receiver": {
    "name": {
      "firstName": "John",
      "lastName": "Doe",
      "companyName": "ACME Corp.",
      "additionalName": "Benelux"
    },
    "address": {
      "countryCode": "NL",
      "postalCode": "3542AD",
      "city": "Utrecht",
      "street": "Reactorweg",
      "additionalAddressLine": "Street part 2 (not applicable for DHL Parcel Benelux)",
      "number": "25",
      "isBusiness": true,
      "addition": "A"
    },
    "email": "mrparcel@dhlparcel.nl",
    "phoneNumber": "0031612345678",
    "vatNumber": "NL007096100B01",
    "eoriNumber": "NL123456789",
    "reference": "Customer reference"
  },
  "shipper": {
    "name": {
      "firstName": "John",
      "lastName": "Doe",
      "companyName": "ACME Corp.",
      "additionalName": "Benelux"
    },
    "address": {
      "countryCode": "NL",
      "postalCode": "3542AD",
      "city": "Utrecht",
      "street": "Reactorweg",
      "additionalAddressLine": "Street part 2 (not applicable for DHL Parcel Benelux)",
      "number": "25",
      "isBusiness": true,
      "addition": "A"
    },
    "email": "mrparcel@dhlparcel.nl",
    "phoneNumber": "0031612345678",
    "vatNumber": "NL007096100B01",
    "eoriNumber": "NL123456789"
  },
  "accountId": "01234567",
  "options": [
    {
      "key": "PS",
      "input": "8004-NL-132825"
    }
  ],
  "pieces": [
    {
      "parcelType": "SMALL",
      "quantity": 1,
      "weight": 1,
      "dimensions": {
        "length": 20,
        "width": 25,
        "height": 30
      }
    }
  ]
}
```
The top-level attributes: ```shipmentId```, ```orderReference```, ```receiver```, ```shipper```, ```options```, etc. are available as **arguments** to the function. These arguments contain either a ```list``` or a ```dict``` of data, depending on what is expected.

We can then create above shipment request as follows:

```python
new_shipment = api.shipments.create(
  shipmentId = "15916857-2a31-4238-a45b-e7ba32e0e320",
  orderReference = "myReference",
  receiver =  {
    "name": {
      "firstName": "John",
      "lastName": "Doe",
      "companyName": "ACME Corp.",
      "additionalName": "Benelux"
    },
    "address": {
      "countryCode": "NL",
      "postalCode": "3542AD",
      "city": "Utrecht",
      "street": "Reactorweg",
      "additionalAddressLine": "Street part 2 (not applicable for DHL Parcel Benelux)",
      "number": "25",
      "isBusiness": true,
      "addition": "A"
    },
    "email": "mrparcel@dhlparcel.nl",
    "phoneNumber": "0031612345678",
    "vatNumber": "NL007096100B01",
    "eoriNumber": "NL123456789",
    "reference": "Customer reference"
  },
  shipper = {
    "name": {
      "firstName": "John",
      "lastName": "Doe",
      "companyName": "ACME Corp.",
      "additionalName": "Benelux"
    },
    "address": {
      "countryCode": "NL",
      "postalCode": "3542AD",
      "city": "Utrecht",
      "street": "Reactorweg",
      "additionalAddressLine": "Street part 2 (not applicable for DHL Parcel Benelux)",
      "number": "25",
      "isBusiness": true,
      "addition": "A"
    },
    "email": "mrparcel@dhlparcel.nl",
    "phoneNumber": "0031612345678",
    "vatNumber": "NL007096100B01",
    "eoriNumber": "NL123456789"
  },
  accountId = "01234567",
  options = [
    {
      "key": "PS",
      "input": "8004-NL-132825"
    }
  ],
  pieces = [
    {
      "parcelType": "SMALL",
      "quantity": 1,
      "weight": 1,
      "dimensions": {
        "length": 20,
        "width": 25,
        "height": 30
      }
    }
  ]
)
```

The response will be put in the ```new_shipment``` object.

### Error handling

Basic error handling has been added. You can check if an error has occured during a call by checking the ```has_error``` attribute on an object. If the ```has_error``` has been set to ```True```, an ```Error``` object will be attached to the ```error``` attribute of the same object. The ```Error``` object contains two attributes: ```returned_content``` and ```status```. ```returned_content``` can be empty as not all errors return something.

```python
shipment = api.shipments.get(id)

if shipment.has_error:
    print(shipment.error.status) # status code
    print(shipment.error.returned_content) # returned content, if any. Can be empty.
```

## Available endpoints & functions

Following endpoints are available:

- capabilities
- shipments
- labels
- parcel_types
- products
- pickup_availablity
- parcelshops

Following functions are available:
- get()
- list()
- create()

Use them as follows:

```python
api.endpoint.function()

# example:
# api.products.get(id)
# api.products.list()
# api.parcelshops.list()
# api.parcelshops.get(id)
# api.shipments.create()
```

All functions are type-hinted and thus should tell you what each function for each endpoints expects. A function that retrieves only one object will always return a ```BaseModel``` object with the returned fields from the response attached as attributes. A list will always return a ```ObjectListModel```, which you can iterate over using the ```.items()``` function. This will return a list of ```BaseModel``` objects.