from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.psql import events, sensors

class Item(BaseModel):
    all_rows : list = []

app = FastAPI(
    title="sensors log app"
)

@app.post("/events/create")
def events_create():
    return [{"events": events.create()}]

@app.post("/events/add")
def events_add(sensor_id: int, name: str, temperature: int = None, humidity: int = None):
    result = events.add(sensor_id, name, temperature, humidity)
    if "sensors" in result[0]: #if return [{"sensors" : 'No such sensor with id = {sensor_id}'}]
        raise HTTPException(status_code=400, detail=result[0]["sensors"])
    else:
        return result
    
@app.delete("/events/delete")
def events_delete(event_id: int):
    result = events.delete(event_id)
    if "events" in result[0]: #if return [{"events" : 'No such event with id = {event_id}'}]
        raise HTTPException(status_code=400, detail=result[0]["events"])
    else:
        return result

@app.post("/events/add_json")
def events_add_json(item : Item):
    result_list = []
    for row in item.all_rows:
        result_list.append(events.add(row["sensor_id"], row["name"], row["temperature"] if "temperature" in row else None, row["humidity"] if "humidity" in row else None)[0])
        print(result_list)
    return result_list

@app.get("/events/show_all")
def events_show_all(start: int = 0, limit: int = None):
    return events.show_all(start, limit)

@app.get("/events/filter_sensor")
def events_filter_sensor(sensor_id: int, start: int = 0, limit: int = None):
    return events.filter_sensor(sensor_id, start, limit)

@app.get("/events/filter_temp_hum")
def events_filter_temp_hum(filter_temperature: str = "> 0", filter_humidity: str = "> 0", start: int = 0, limit: int = None):
    try:
        return events.filter_temp_hum(filter_temperature, filter_humidity, start, limit)
    except Exception as _ex:
        raise HTTPException(status_code=400, detail="Bad filter_temperature or filter_humidity")

@app.delete("/events/drop")
def events_drop():
    try:
        return [{"events": events.drop()}]
    except Exception as _ex:
        raise HTTPException(status_code=400, detail="Cant drop")

@app.post("/sensors/create")
def sensors_create():
    return [{"sensors": sensors.create()}]

@app.get("/sensors/show_all")
def sensors_show_all(start: int = 0, limit: int = None):
    return sensors.show_all(start, limit)

@app.post("/sensors/add")
def sensors_add(sensor_id: int, sensor_type: int, sensor_name: str = None):
    if (sensor_type > 3 or sensor_type < 1):
        raise HTTPException(status_code=400, detail='type should be >= 1 and <= 3') 
    else: 
        result = sensors.add(sensor_id, sensor_type, sensor_name)
        if result is None:
            raise HTTPException(status_code=400, detail='id already exist')
        else:
            return result
        
@app.delete("/sensors/delete")
def sensors_delete(sensor_id: int):
    result = sensors.delete(sensor_id)
    if "sensors" in result[0]: #if return [{"sensors" : 'No such sensor with id = {sensor_id}'}]
        raise HTTPException(status_code=400, detail=result[0]["sensors"])
    else:
        return result

@app.delete("/sensors/drop")
def sensors_drop():
    try:
        return [{"events": sensors.drop()}]
    except Exception as _ex:
        raise HTTPException(status_code=400, detail="Cant drop")

@app.get("/")
def test_task():
    return "test_task"