import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from flaskext.mysql import MySQL
import pymysql
import logging
import sys
from pathlib import Path
import uuid

app = Flask(__name__)
db = pymysql.connect(host='localhost',
                     user='root',
                     password='Jubilant9828!',
                     db='enable_ninja_local')

app = Flask(__name__)
app.config.from_object(__name__)
deviceID = 0
apiUrl = "/api/v1/"
# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

#  index method to create a file if it doesn't exist that will hold the device id


@app.route(f'{apiUrl}index', methods=['GET'])
def index():
    global deviceID

    if request.method == 'GET':
        try:
            # this is for the first time load only to create the file
            # check if the device config file exists if not create it and write the device id to it
            if not Path("device_config.txt").is_file():
                with open("device_config.txt", "w") as f:
                    deviceID = str(uuid.uuid4())
                    f.write(deviceID)
                    f.close()

                    # insert device id into the device table
                    cursor = db.cursor()
                    sql = "INSERT INTO device (device_id) VALUES (%s)"
                    val = (deviceID,)
                    cursor.execute(sql, val)
            else:
                # read the device id from the file
                with open("device_config.txt", "r") as f:
                    deviceID = f.read()
                    f.close()

            # query to check to see if the device id has an account associated with it
            cursor = db.cursor()
            sql = "SELECT * FROM device WHERE device_id = %s"
            val = (deviceID,)
            cursor.execute(sql, val)
            result = cursor.fetchone()
            return jsonify(result)
        except Exception as e:
            print(e)
            return jsonify({"error": f"An error occurred in the index method with exception ({e})"})


# sanity check route
@app.route(f'{apiUrl}add-session', methods=['POST'])
def add_session():
    
    if request.method == 'POST':
        try:
            results = []
            form = request.get_json(silent=True).get('form')
            cursor = db.cursor()
            for i in form:
                # insert data in database
                cursor.execute(
                    "INSERT INTO `enable_ninja_local`.track_session (created_date, average_lap, fastest_lap) VALUES (%s, %s, %s)",
                    (i['sessionDate'], i['avgLap'], i['fastestLap']))
                db.commit()

                # get last inserted id
                cursor.execute(
                    "SELECT SESSION_ID FROM `enable_ninja_local`.track_session ORDER BY SESSION_ID DESC LIMIT 1")
                seshID = cursor.fetchone()[0]
                print(seshID)

                # insert data in lap table
                for j in i['laps']:
                    cursor.execute(
                        "INSERT INTO `enable_ninja_local`.lap (track_session_id, lap_number, lap_time, lap_time_diff) VALUES (%s, %s, %s, %s)",
                        (int(seshID), j['lap'], j['time'], j['timeDiff']))
                    db.commit()
            results = cursor.fetchall()
            return jsonify(results)
        except Exception as e:
            print(e)
            return jsonify({"error": ("An error occurred in the add_session method with exception (%s)", e)})


if __name__ == '__main__':
    app.run()
