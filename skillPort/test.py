from flask import Flask, rendeer_template, request
import mysql.connector
import math


app = Flask(__name__)

def connect_db():
    con = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = '',
        db = 'oppai',

    )
    return con