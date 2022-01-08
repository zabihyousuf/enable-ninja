from datetime import time
import logging
from flask import Flask, jsonify, request
import time
from multiprocessing import Process, Value
from flask_cors import CORS
from flaskext.mysql import MySQL
import pymysql
import logging
import sys
from pathlib import Path
import uuid
import os 
# initial app set up
app = Flask(__name__)

# local host db config
localhostConfig = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Jubilant9828!',
    'db': 'enable_ninja_local'
}

# main config for production
mainConfig = {
    'host': 'enable-ninja-main.cnecu7z7uv6q.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'password123',
    'db': 'enable_ninja_local'
}

finaList = []
# main db connection
# db = pymysql.connect(**mainConfig)

# local db connection
db = pymysql.connect(**localhostConfig)

app = Flask(__name__)
app.config.from_object(__name__)


# device config api 
deviceID = 0
apiUrl = "/api/v1/"


# get device_config.txt file path
path = os.getcwd()
name = "device_config.txt"

deviceUrl = "device_config.txt"


# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route(f'{apiUrl}index', methods=['GET'])
def index():
    """
    This is the index page for the API.
    :return:
        success or error message
    """
    recording_on = Value('b', True)
    p = Process(target=record_loop, args=(recording_on,))
    p.start()  
    global deviceID
    if request.method == 'GET':
        try:
            # this is for the first time load only to create the file
            # check if the device config file exists if not create it and write the device id to it
            if not Path(deviceUrl).is_file():
                with open(deviceUrl, "w") as f:
                    deviceID = str(uuid.uuid4())
                    f.write(deviceID)
                    f.close()

                    # insert device id into the device table
                    cursor = db.cursor()
                    sql = "INSERT INTO `enable_ninja_local`.device_x_user (device_id) VALUES (%s)"
                    val = (deviceID)
                    cursor.execute(sql, val)
                    db.commit()
            else:
                # read the device id from the file
                with open(deviceUrl, "r") as f:
                    deviceID = f.read()
                    f.close()

            # query to check to see if the device id has an account associated with it
            cursor = db.cursor()
            sql = "SELECT * FROM `enable_ninja_local`.device_x_user WHERE DEVICE_ID = %s"
            val = (deviceID)
            cursor.execute(sql, val)
            result = cursor.fetchone()
            return jsonify(result)
        except Exception as e:
            print(e)
            return jsonify({"error": f"An error occurred in the index method with exception ({e})"})



@app.route(f'{apiUrl}add-session', methods=['POST'])
def add_session():
    """
    This method is used to add a new session to the database

    :return:
        either a json object with the session id or an error message
    """
    if request.method == 'POST':
        try:
            results = []
            form = request.get_json(silent=True).get('form')
            cursor = db.cursor()
            for i in form:
                # insert data in database
                cursor.execute(
                    "INSERT INTO `enable_ninja_local`.track_session (created_date, average_lap, fastest_lap, device_id) VALUES (%s, %s, %s, %s)",
                    (i['sessionDate'], i['avgLap'], i['fastestLap'], deviceID))
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

def record_loop(loop_on):
    global finaList
    while True:
        if loop_on.value == True:
            finaList.append(time.time())
            print(finaList)
        time.sleep(.5)

if __name__ == '__main__':
    
    app.run()
