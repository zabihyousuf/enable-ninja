from crypt import methods
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
# main config for production
mainConfig = {
    'host': 'enable-ninja-main.cnecu7z7uv6q.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'Jubilant3554',
    'db': 'enable_ninja_local'
}

db = pymysql.connect(**mainConfig)
finalList = []
with open('track_list.txt', 'r') as f:
    for line in f:
        finalList.append(line.strip().split(','))
for i in finalList:
    print(i)
    with db.cursor() as cursor:
        sql = "INSERT INTO `enable_ninja_local`.`tracks` (`track_name`, `track_latitude`, `track_longitude`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (i[0], i[1], i[2]))
        db.commit()