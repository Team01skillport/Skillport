from flask import Flask, render_template, request, session, redirect, url_for
import mysql.connector
import math
import json
import os

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")

if __name__ == "__main__":
  app.debug = True
  app.run(host = "localhost", port=5000)