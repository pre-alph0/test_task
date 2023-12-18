# sensors log app

Ensure that all necessary libraries are imported from `requirements.txt` 

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

    curl -X 'POST' \
    'http://127.0.0.1:8000/sensors/create' \
    -H 'accept: application/json' \
    -d ''
  ### Response
    HTTP/1.1" 200 OK
    
    [
      {
        "events": "created"
      }
    ]
