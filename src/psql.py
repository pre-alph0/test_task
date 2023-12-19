import psycopg2
from src.config import host, user, db_name, password

def null_if_None(variable):
    if variable is None:
        return 'null'
    else:
        return variable

class events_table():
    def __init__(self, cursor):
        self.cursor = cursor

    def json_result(self, fetch): #make result structure same as events.json 
        dic = {}
        list_data = []
        for x in fetch:
            dic['sensor_id'] = x[0]
            dic['name'] = x[1]
            dic['temperature'] = x[2]
            dic['humidity'] = x[3]
            if len(x) > 4: #if trying to handle fetch after join sensors_table and sevents_table
                dic['sensor_type'] = x[4]
                dic['sensor_name'] = x[5]
            list_data.append(dic.copy())
        return list_data

    def create(self):
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS events(
                id serial PRIMARY KEY,
                sensor_id INT NOT NULL,
                name varchar(50) NOT NULL,
                temperature INT NULL,
                humidity INT NULL);"""
        )
        return "created"
    
    def add(self, sensor_id, name, temperature, humidity):
        cursor.execute(""" SELECT id
                       FROM sensors
                       WHERE id = %s;""",   (sensor_id, ))
        if cursor.fetchone() is None: return [{'sensors' : f'No such sensor with id = {sensor_id}'}]  #no sensor_id in sensors 
        else: 
            cursor.execute(f""" INSERT INTO events(sensor_id, name, temperature, humidity) VALUES ({sensor_id}, '{name}', {null_if_None(temperature)}, {null_if_None(humidity)})
                       ON CONFLICT DO NOTHING RETURNING * """)
            fetch = cursor.fetchone()
            fetch_result = [fetch[1:]] #skip id which is not needed
            return self.json_result(fetch_result)
        
    def delete(self, event_id):
        cursor.execute(""" SELECT id
                       FROM events
                       WHERE id = %s;""",   (event_id, ))
        if cursor.fetchone() is None: return [{'events' : f'No such event with id = {event_id}'}]  #no id in events 
        else: 
            cursor.execute(f""" DELETE 
                                FROM events
                                WHERE id = {event_id}
                                RETURNING *; """)
            fetch = cursor.fetchone()
            fetch_result = [fetch[1:]] #skip id which is not needed
            return self.json_result(fetch_result)
    
    def show_all(self, start, limit):
        if limit is None: cursor.execute(f"""SELECT events.sensor_id, events.name, events.temperature, events.humidity, sensors.type AS sensor_type, sensors.name AS sensor_name 
                                              FROM events
                                              LEFT JOIN sensors ON events.sensor_id = sensors.id 
                                              WHERE events.id > {start} ORDER BY events.id ASC;""")
        else: cursor.execute(f"""SELECT events.sensor_id, events.name, events.temperature, events.humidity, sensors.type AS sensor_type, sensors.name AS sensor_name 
                                FROM events
                                LEFT JOIN sensors ON events.sensor_id = sensors.id 
                                WHERE events.id > {start} ORDER BY events.id ASC LIMIT {limit};""")
        fetch = cursor.fetchall()
        return self.json_result(fetch)
    
    def filter_sensor(self, filter_sensor_id, start, limit): #TODO: filter by name
        if limit is None: cursor.execute(f"""SELECT sensor_id, name, temperature, humidity, sensor_type, sensor_name 
                                FROM ( SELECT events.sensor_id, events.name, events.temperature, events.humidity, sensors.type AS sensor_type, sensors.name AS sensor_name, ROW_NUMBER() OVER(PARTITION BY events.sensor_id ORDER BY events.id)
                                     FROM events
                                     LEFT JOIN sensors ON events.sensor_id = sensors.id 
                                )events1
                                WHERE sensor_id = {filter_sensor_id} and row_number > {start};""")
        else: cursor.execute(f"""SELECT sensor_id, name, temperature, humidity, sensor_type, sensor_name 
                                FROM ( SELECT events.sensor_id, events.name, events.temperature, events.humidity, sensors.type AS sensor_type, sensors.name AS sensor_name, ROW_NUMBER() OVER(PARTITION BY events.sensor_id ORDER BY events.id)
                                     FROM events
                                     LEFT JOIN sensors ON events.sensor_id = sensors.id 
                                )events1
                                WHERE sensor_id = {filter_sensor_id} and row_number > {start} LIMIT {limit};""")
        fetch = cursor.fetchall()
        return self.json_result(fetch)
    
    def filter_temp_hum(self, filter_temperature, filter_humidity, start, limit):
        cursor.execute(f"""SELECT events.sensor_id, events.name, events.temperature, events.humidity, sensors.type AS sensor_type, sensors.name AS sensor_name 
                                FROM events
                                LEFT JOIN sensors ON events.sensor_id = sensors.id 
                                WHERE temperature {filter_temperature} and humidity {filter_humidity}; """)
        fetch = cursor.fetchall() 
        if limit is None: 
            limit = len(fetch)
        return self.json_result(fetch[start:start+limit])

    def drop(self):
        cursor.execute(
                """DROP TABLE events;"""
            )
        return "deleted"

class sensors_table():
    def __init__(self, cursor):
        self.cursor = cursor

    def json_result(self, fetch): #make result structure same as events.json 
        dic = {}
        list_data = []
        for x in fetch:
            dic['id'] = x[0]
            dic['name'] = x[1]
            dic['type'] = x[2]
            list_data.append(dic.copy())  
        return list_data

    def create(self):
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS sensors(
                id serial PRIMARY KEY,
                name varchar(50) NULL,
                type INT NOT NULL CHECK (type >= 1 AND type <= 3));"""
        )
        return "created"
    
    def add(self, sensor_id, type, name):
        if name is None:
            cursor.execute(f""" INSERT INTO sensors(id, type, name) VALUES ({sensor_id}, {type}, null)
                    ON CONFLICT DO NOTHING RETURNING * """)
        else:
            cursor.execute(f""" INSERT INTO sensors(id, type, name) VALUES ({sensor_id}, {type}, '{name}')
                        ON CONFLICT DO NOTHING RETURNING * """)
        fetch = cursor.fetchone()
        if fetch is None: 
            return None 
        else:
            return self.json_result([fetch])
        
    def delete(self, sensor_id):
        cursor.execute(""" SELECT id
                       FROM sensors
                       WHERE id = %s;""",   (sensor_id, ))
        if cursor.fetchone() is None: 
            return [{'sensors' : f'No such sensor with id = {sensor_id}'}]  #no id in sensors 
        else: 
            cursor.execute(f""" DELETE 
                                FROM sensors
                                WHERE id = {sensor_id}
                                RETURNING *; """)
            fetch = cursor.fetchone()
            fetch_result = [fetch] #skip id which is not needed
            return self.json_result(fetch_result)
        
    def show_all(self, start, limit):
        if limit is None: cursor.execute(f"""SELECT id, name, type
                                            FROM ( SELECT *, ROW_NUMBER() OVER (ORDER BY 1) AS row_number
                                            FROM sensors
                                            )sensors1
                                            WHERE row_number > {start}  ORDER BY row_number ASC;""")
        else: cursor.execute(f"""SELECT id, name, type
                                            FROM ( SELECT *, ROW_NUMBER() OVER (ORDER BY 1) AS row_number
                                            FROM sensors
                                            )sensors1
                                            WHERE row_number > {start}  ORDER BY row_number ASC LIMIT {limit};""")
        fetch = cursor.fetchall()
        return self.json_result(fetch)

    def drop(self):
        cursor.execute(
                """DROP TABLE sensors;"""
            )
        return "deleted"

try:
    # connect to exist database
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name    
    )
    connection.autocommit = True
        
    cursor =  connection.cursor()

    events = events_table(cursor)
    sensors = sensors_table(cursor)
    
except Exception as _ex:
    print("[INFO] Error while connecting with PostgreSQL", _ex)