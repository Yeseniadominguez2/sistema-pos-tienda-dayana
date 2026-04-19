from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from core.config import DB_CONFIG


def conectar():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a MySQL:\n{e}")
        return None


def ejecutar(sql, params=None, fetchall=False, fetchone=False):
    conn = conectar()
    if not conn:
        return None
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params or ())
        if fetchall:
            return cur.fetchall()
        if fetchone:
            return cur.fetchone()
        conn.commit()
        return cur.lastrowid
    except Error as e:
        messagebox.showerror("Error SQL", str(e))
        return None
    finally:
        conn.close()