from flask import Blueprint, render_template, request, make_response
import mysql.connector
from mysql.connector import Error
def connect_db():
    try:
        con = mysql.connector.connect(
        host="localhost",
        user = "root",
        passwd = "",
        db = "skillport_db"
        )
        
        if con.is_connected():
            print("Windows設定で接続完了")
            return con
        
    except Error as e:
        print("Windows設定で接続失敗", e)
        
    try:
        con = mysql.connector.connect(
        host="localhost",
        port = 8889,
        user = "root",
        passwd = "root",
        db = "skillport_db"
        )
        
        if con.is_connected():
            print("MAC設定で接続完了")
            return con
    except Error as e:
        print("MAC設定で接続失敗", e)
        
    raise ConnectionError("DBへの接続失敗")
        
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

def create_user(sql, params=None):
    try:
        con = connect_db()
        cur = con.cursor(dictionary=True)
        cur.execute(sql, params)
        con.commit()
        cur.close()
        con.close()
        return True 
    except Exception as e: 
        print(f"データベースエラー: {e}")
        con.rollback()
        cur.close()
        con.close()
        return None
    
def execute_query(sql, params=None):
    try:
        con = connect_db()
        cur = con.cursor(dictionary=True)
        cur.execute(sql, params)
        con.commit() # 提交
        cur.close()
        con.close()
        return True 
    except Exception as e: 
        print(f"データベースエラー: {e}")
        con.rollback() # 回滚
        cur.close()
        con.close()
        return None