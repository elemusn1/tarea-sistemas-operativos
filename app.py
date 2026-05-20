from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__, template_folder='.')

DB_FILE = "database.db"

def consultar_db(query, args=(), fetch=False):
    """Función segura para conectar, asegurar la tabla y ejecutar consultas."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Aseguramos la tabla SIEMPRE antes de cualquier operación
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT
        )
    ''')
    cursor.execute(query, args)
    resultado = None
    if fetch:
        resultado = cursor.fetchall()
    conn.commit()
    conn.close()
    return resultado

@app.route('/')
def index():
    """Capa de Datos -> Capa de Presentación: Lee las tareas asegurando la tabla."""
    try:
        tareas = consultar_db("SELECT * FROM tareas ORDER BY id DESC", fetch=True)
        return render_template('index.html', tareas=tareas)
    except Exception as e:
        return f"Error en la base de datos: {str(e)}", 500

@app.route('/agregar', methods=['POST'])
def agregar_tarea():
    """Recibe los datos del frontend y los guarda de forma segura."""
    titulo = request.form.get('titulo')
    descripcion = request.form.get('descripcion')
    
    if titulo:
        consultar_db("INSERT INTO tareas (titulo, descripcion) VALUES (?, ?)", (titulo, descripcion))
        
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
