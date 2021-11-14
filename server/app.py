import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from flaskext.mysql import MySQL
import pymysql
import logging
import sys

app = Flask(__name__)
db = pymysql.connect(host='localhost',
                     user='root',
                     password='Jubilant9828!',
                     db='enable_ninja_local')
# configuration
# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})


# sanity check route
@app.route('/api/v1/add-session', methods=['POST'])
def add_session():
    results = []
    logging.warning("See this message in Flask Debug Toolbar!")
    if request.method == 'POST':
        form = request.get_json(silent=True).get('form')
        cursor = db.cursor()
        # # cursor.execute(hello_world())
        for i in form:
            # insert data in database
            cursor.execute(
                "INSERT INTO `enable_ninja_local`.track_session (created_date, average_lap, fastest_lap) VALUES (%s, %s, %s)",
                (i['sessionDate'], i['avgLap'], i['fastestLap']))
            db.commit()

            #get last inserted id
            cursor.execute("SELECT SESSION_ID FROM `enable_ninja_local`.track_session ORDER BY SESSION_ID DESC LIMIT 1")
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


def hello_world():
    return 'select * from `enable_ninja_local`.track_session'


if __name__ == '__main__':
    app.run()