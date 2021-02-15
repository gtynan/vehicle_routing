# Pickup and delivery scheduler

Quick API implementation of Google ORTools used to schedule drivers [LINK](https://developers.google.com/optimization/routing). 

Given a distance matrix find the optimal routes to minimise total distance traveled.  


## Usage 

**Sample Request**

`POST /schedule/create`

- Distance matrix and pickup/delivery requirements passed in data

```
http://127.0.0.1:8000/schedule/create?n_vehicles=3&depot_node=0
```

**Sample Response**

- `id` refers to route order so `id=0` is the first route for a driver
- `start` and `end` refers to a location in this instance `name` is just referencing their index in the distance matrix

```
[
  {
    "driver": {
      "name": "0"
    },
    "routes": [
      {
        "id": 0,
        "start": {
          "name": "0"
        },
        "end": {
          "name": "5"
        }
      },
      {
        "id": 1,
        "start": {
          "name": "5"
        },
        "end": {
          "name": "4"
        }
      },
      {
        "id": 2,
        "start": {
          "name": "4"
        },
        "end": {
          "name": "3"
        }
      },
      {
        "id": 3,
        "start": {
          "name": "3"
        },
        "end": {
          "name": "11"
        }
      },
      {
        "id": 4,
        "start": {
          "name": "11"
        },
        "end": {
          "name": "12"
        }
      },
      {
        "id": 5,
        "start": {
          "name": "12"
        },
        "end": {
          "name": "9"
        }
      },
      {
        "id": 6,
        "start": {
          "name": "9"
        },
        "end": {
          "name": "0"
        }
      }
    ]
  },
  {
    "driver": {
      "name": "1"
    }
    ...
```

## Todo
- Use google maps distance API
- Extened optional settings
