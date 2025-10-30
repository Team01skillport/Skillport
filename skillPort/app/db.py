from flask import Blueprint, render_template, request, make_response
import mysql.connector
def connect_db():
    con = mysql.connector.connect(
    host="localhost",
    port = 8889,
    user = "root",
    passwd = "root",
    db = "skillport_db"
    )
    return con
    
def fetch_query(sql,params=None,fetch_one=False):
    try:
        con = connect_db()
        cur = con.cursor(dictionary=True)
        cur.execute(sql, params)
        if fetch_one == False:
            result = cur.fetchall()
        else:
            result = cur.fetchone()
        cur.close()
        con.close()
    except Exception as e:
        print(f"データベースエラー: {e}")
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