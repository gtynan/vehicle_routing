# Pickup/Delivery management 

API implementation of Google Ortools to handle fleet management. 


## Sample Usage


### Create a time matrix

A time matrix represents the duration between each location specified

**Request**

`POST /time_matrix/create` 

Params:
- return_home: True (whether or not to include distance back to drivers starting point)

Data:
- locations: 
    
    [ "12 Glendoher Road, Rathfarnham, Dublin 16",

    "446A, North Circular Road, Dublin 1",
    
    "52 Hillcourt Road, Glenageary, Co Dublin",
    
    "6 The Ramparts, Cabinteely, Dublin 18,",
    
    "127 Ballyroan Road, Rathfarnham, Dublin 16" ]

- driver_indicies: [0] (location indicies that refers to drivers starting position)

**Response**

```json
{
  "locations": [
    "12 Glendoher Road, Rathfarnham, Dublin 16",
    "446A, North Circular Road, Dublin 1",
    "52 Hillcourt Road, Glenageary, Co Dublin",
    "6 The Ramparts, Cabinteely, Dublin 18,",
    "127 Ballyroan Road, Rathfarnham, Dublin 16"
  ],
  "driver_indicies": [
    0
  ],
  "matrix": [
    [
      0,
      1467,
      1366,
      1044,
      108
    ],
    [
      1392,
      0,
      2148,
      1827,
      1396
    ],
    [
      1402,
      2093,
      0,
      597,
      1441
    ],
    [
      1219,
      1910,
      659,
      0,
      1257
    ],
    [
      112,
      1359,
      1383,
      1062,
      0
    ]
  ]
}
```

### Create driver schedule

**Request**

`POST /schedule/create` 

Params:
- max_time: 28800

Data:
- time_matrix: **see above**
- driver_indicies: **see above**
- location_names: **see above**
- delivery_pairs: 
    [
        [2, 4],   [3, 1]
    ]
- *Optionals*:
    - *delivery_weights*: if multiple vehicles and not every vehicle can handle every delivery
    - *vehicle_capacities*: max capacity, will not schedule a job where delivery exceeds this value
    - *site_eta*: specify time spent at a location before being able to leave


**Response**

```json
[
  {
    "driver": {
      "id": 0
    },
    "route": [
      {
        "id": 0,
        "start": {
          "name": "12 Glendoher Road, Rathfarnham, Dublin 16"
        },
        "end": {
          "name": "6 The Ramparts, Cabinteely, Dublin 18,"
        },
        "duration": 1044,
        "arrival_time": "14:00:26.465822"
      },
      {
        "id": 1,
        "start": {
          "name": "6 The Ramparts, Cabinteely, Dublin 18,"
        },
        "end": {
          "name": "446A, North Circular Road, Dublin 1"
        },
        "duration": 1910,
        "arrival_time": "14:32:16.465987"
      },
      {
        "id": 2,
        "start": {
          "name": "446A, North Circular Road, Dublin 1"
        },
        "end": {
          "name": "52 Hillcourt Road, Glenageary, Co Dublin"
        },
        "duration": 2148,
        "arrival_time": "15:08:04.466088"
      },
      {
        "id": 3,
        "start": {
          "name": "52 Hillcourt Road, Glenageary, Co Dublin"
        },
        "end": {
          "name": "127 Ballyroan Road, Rathfarnham, Dublin 16"
        },
        "duration": 1441,
        "arrival_time": "15:32:05.466148"
      },
      {
        "id": 4,
        "start": {
          "name": "127 Ballyroan Road, Rathfarnham, Dublin 16"
        },
        "end": {
          "name": "12 Glendoher Road, Rathfarnham, Dublin 16"
        },
        "duration": 112,
        "arrival_time": "15:33:57.466200"
      }
    ]
  }
]
```
