from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
DB_PATH = "residentes.db"

# --- Crear base de datos si no existe ---
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS viveres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                fecha_ingreso TEXT,
                producto TEXT,
                cantidad INTEGER,
                fecha_vencimiento TEXT,
                bienes TEXT,
                utilidad TEXT
            )
        ''')
        conn.commit()

# --- Obtener todos los registros ---
def obtener_viveres():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM viveres")
        return cursor.fetchall()

# --- Agregar un registro ---
def agregar_viveres(nombre, fecha_ingreso, producto, cantidad, fecha_vencimiento, bienes, utilidad):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO viveres (nombre, fecha_ingreso, producto, cantidad, fecha_vencimiento, bienes, utilidad)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nombre, fecha_ingreso, producto, cantidad, fecha_vencimiento, bienes, utilidad))
        conn.commit()

# --- Obtener un registro por ID ---
def obtener_por_id(viver_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM viveres WHERE id = ?", (viver_id,))
        return cursor.fetchone()

# --- Actualizar un registro ---
def actualizar_viveres(viver_id, nombre, fecha_ingreso, producto, cantidad, fecha_vencimiento, bienes, utilidad):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE viveres
            SET nombre=?, fecha_ingreso=?, producto=?, cantidad=?, fecha_vencimiento=?, bienes=?, utilidad=?
            WHERE id=?
        """, (nombre, fecha_ingreso, producto, cantidad, fecha_vencimiento, bienes, utilidad, viver_id))
        conn.commit()

# --- Eliminar un registro ---
def eliminar_viveres(viver_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM viveres WHERE id=?", (viver_id,))
        conn.commit()

# --- Rutas Flask ---
@app.route('/')
def index():
    registros = obtener_viveres()
    return render_template('inicio.html', registros=registros)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form['nombre']
    fecha_ingreso = request.form['fecha_ingreso']
    producto = request.form['producto']
    cantidad = request.form['cantidad']
    fecha_vencimiento = request.form['fecha_vencimiento']
    bienes = request.form['bienes']
    utilidad = request.form['utilidad']
    agregar_viveres(nombre, fecha_ingreso, producto, cantidad, fecha_vencimiento, bienes, utilidad)
    return redirect('/')

@app.route('/editar/<int:viver_id>')
def editar(viver_id):
    registro = obtener_por_id(viver_id)
    return render_template('editar.html', registro=registro)

@app.route('/actualizar/<int:viver_id>', methods=['POST'])
def actualizar(viver_id):
    nombre = request.form['nombre']
    fecha_ingreso = request.form['fecha_ingreso']
    producto = request.form['producto']
    cantidad = request.form['cantidad']
    fecha_vencimiento = request.form['fecha_vencimiento']
    bienes = request.form['bienes']
    utilidad = request.form['utilidad']
    actualizar_viveres(viver_id, nombre, fecha_ingreso, producto, cantidad, fecha_vencimiento, bienes, utilidad)
    return redirect('/')

@app.route('/eliminar/<int:viver_id>')
def eliminar(viver_id):
    eliminar_viveres(viver_id)
    return redirect('/')

# --- Inicializar base de datos y ejecutar app ---
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
