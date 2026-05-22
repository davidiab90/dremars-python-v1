from flask import Flask, render_template, request, jsonify
import requests
import base64
import os
import traceback
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Crea DB una sola vez (module level)
conn = sqlite3.connect('static/db_leads.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS leads (id INTEGER PRIMARY KEY, name TEXT, email TEXT, message TEXT, date TEXT)''')
conn.commit()
conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    success = False
    error = None

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', 'Consulta general').strip()

        if not name or not email:
            error = "Nombre y email son obligatorios."
        else:
            db_dir = 'static'
            db_path = os.path.join(db_dir, 'db_leads.db')

            # Crea carpeta static si no existe
            os.makedirs(db_dir, exist_ok=True)

            try:
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                c.execute('''CREATE TABLE IF NOT EXISTS leads 
                             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                              name TEXT NOT NULL, 
                              email TEXT NOT NULL, 
                              message TEXT, 
                              date TEXT)''')
                c.execute("INSERT INTO leads (name, email, message, date) VALUES (?, ?, ?, ?)", 
                          (name, email, message, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                conn.commit()
                conn.close()
                success = True
            except Exception as e:
                error = "Error al guardar. Intenta de nuevo."
                print(f"Error DB: {e}")

    return render_template('contact.html', success=success, error=error)

@app.route('/project_original_designs')
def project_original_designs():
    return render_template('project_original_designs.html')

@app.route('/project_physical_projects')
def project_physical_projects():
    return render_template('project_physical_projects.html')

@app.route('/project_interior_plans')
def project_interior_plans():
    return render_template('project_interior_plans.html')

@app.route('/services')
def services():
    return render_template('services.html')

app.config['TEMPLATES_AUTO_RELOAD'] = True

application = app

if __name__ == "__main__":
    app.run(debug=True)