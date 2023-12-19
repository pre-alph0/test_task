# Sensors log app

Ensure that all necessary libraries are imported from `requirements.txt` 

Check full docs at `http://127.0.0.1:8000/docs#`, via __Swagger UI__

## Run the app

    uvicorn src.main:app --reload
    
# Create tables
  Before working with postgresql tables make sure that you created it

  ## Create events table
  `POST /events/create`

    curl -X 'POST' 'http://127.0.0.1:8000/events/create' -H 'accept: application/json' -d ''
  ### Response
    HTTP/1.1" 200 OK
    
    [
      {
        "events": "created"
      }
    ]
  If table already exist, will response same.
  Creates only if table doesnt exist.
  ## Create sensors table
  `POST /sensors/create`

    curl -X 'POST' 'http://127.0.0.1:8000/sensors/create' -H 'accept: application/json' -d ''
  ### Response
    HTTP/1.1" 200 OK
    
    [
      {
        "events": "created"
      }
    ]
  If table already exist, will response same.
  Creates only if table doesnt exist.
# Some features
Here would be some features you should pay attention for. Full docs at `http://127.0.0.1:8000/docs#`    
## GET
- For all `GET` you can set pagination by `start` and `limit`
- `/events/show_all` will return all __events__(without event id column) joined with sensors __name__ and __type__ 
- You can filter __events__ by __temperature__ and __humidity__ by `> {value}`, `>= {value}`, `< {value}`, `<= {value}`\
For example: `curl -X 'GET' 'http://127.0.0.1:8000/events/filter_temp_hum?filter_temperature=%3E%201&filter_humidity=%3E%201&start=0' -H 'accept: application/json'` will filter __temperature > 1__, __humidity__ > 1__
## POST
- `/events/add` will check if __sensor_id__ exist in __sensors__. If true: will return your added row. If false: will rerurn code: 400
- `/sensors/add` will check if __id__ exist in __sensors__. If true: will return your added row. If false: will rerurn code: 400
- You can add info to events from events.json by `curl -X 'POST' 'http://127.0.0.1:8000/events/add_json' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"all_rows": {events.json}`
  If there were some __sensor_id__ thats not in __sensors__, will return:
  `[
  {
    "sensors": "No such sensor with id = 1"
  },
  {
    "sensor_id": 2,
    "name": "N/A",
    "temperature": null,
    "humidity": null
  }
  ]` for example
## DELETE
- You can delete any row by id via `/events/delete` or `/sensors/delete`. If row with such __id__ doesnt exist, will rerurn code: 400
- You can delete any table via `/events/drop` or `/sensors/drop`
