from flask import Blueprint, render_template, request, make_response
import mysql.connector
def connect_db():
    con = mysql.connector.connect(
    host="localhost",
    user = "root",
    passwd = "",
    db = "skillport_db"
    )
    return con
    
def fetch_query(sql, fetch_one=False):
    try:
        con = connect_db()
        cur = con.cursor(dictionary=True)
        cur.execute(sql)
        if fetch_one == False:
            result = cur.fetchall()
        else:
            result = cur.fetchone()
        cur.close()
        con.close()
    except:
        result = None
    return result

def create_user(sql):
    try:
        con = connect_db()
        cur = con.cursor(dictionary=True)
        cur.execute(sql)
        cur.close()
        con.close()
    except:
        return None