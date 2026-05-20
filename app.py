from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__, template_folder='.')

DB_FILE = "database.db"

def init_db():
    """Inicializa la base de datos y crea la tabla si no existe."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Capa de Datos -> Capa de Presentación: Lee las tareas y las muestra."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tareas ORDER BY id DESC")
    tareas = cursor.fetchall()
    conn.close()
    return render_template('index.html', tareas=tareas)

@app.route('/agregar', methods=['POST'])
def agregar_tarea():
    """Recibe los datos del frontend y los guarda en la base de datos."""
    titulo = request.form.get('titulo')
    descripcion = request.form.get('descripcion')
    
    if titulo:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tareas (titulo, descripcion) VALUES (?, ?)", (titulo, descripcion))
        conn.commit()
        conn.close()
        
    return redirect('/')

if __name__ == '__main__':
    init_db()
    # Configuración limpia para el puerto de la nube
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
