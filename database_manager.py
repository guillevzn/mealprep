import sqlite3
import csv

import sqlite3
import csv

def create_database():
    conn = sqlite3.connect('mealprep.db')
    cursor = conn.cursor()
    
    # Crear tabla de recetas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        Id INTEGER PRIMARY KEY,
        Categoria TEXT,
        Nombre TEXT,
        Valoracion INTEGER,
        Dificultad TEXT,
        Num_comensales INTEGER,
        Tiempo TEXT,
        Tipo TEXT,
        Link_receta TEXT,
        Num_comentarios INTEGER,
        Num_reviews INTEGER,
        Fecha_modificacion TEXT,
        Ingredientes TEXT
    )
    ''')
    
    # Crear tabla de historial
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS history (
        Id INTEGER PRIMARY KEY,
        Fecha TEXT,
        Receta_Id INTEGER,
        FOREIGN KEY(Receta_Id) REFERENCES recipes(Id)
    )
    ''')
    
    conn.commit()
    conn.close()

def upload_csv_to_db(filename):
    conn = sqlite3.connect('mealprep.db')
    cursor = conn.cursor()
    
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter='|')
        next(reader)  # Skip header row
        for row in reader:
            cursor.execute('INSERT INTO recipes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', row)
    
    conn.commit()
    conn.close()
 
def get_available_recipes():
    conn = sqlite3.connect('mealprep.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM recipes WHERE Id NOT IN (SELECT Receta_Id FROM history)
    ''')
    
    available_recipes = cursor.fetchall()
    conn.close()
    
    return available_recipes

def add_to_history(recipe_id):
    conn = sqlite3.connect('mealprep.db')
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO history (Fecha, Receta_Id) VALUES (CURRENT_DATE, ?)', (recipe_id,))
    
    conn.commit()
    conn.close()

def clear_history():
    conn = sqlite3.connect('mealprep.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM history')
    
    conn.commit()
    conn.close()

def get_all_recipes():
    conn = sqlite3.connect('mealprep.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM recipes')
    
    all_recipes = cursor.fetchall()
    conn.close()
    
    return all_recipes

def get_unique_values(column_name):
    conn = sqlite3.connect('mealprep.db')
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT DISTINCT {column_name} FROM recipes")
    values = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return values

def get_filtered_recipes(preferencias_categoria=[], preferencias_dificultad=[]):
    conn = sqlite3.connect('mealprep.db')
    cursor = conn.cursor()
    
    query = "SELECT * FROM recipes WHERE 1"
    
    if preferencias_categoria:
        category_conditions = " OR ".join([f"Categoria LIKE '%{cat.strip()}%'" for cat in preferencias_categoria])
        query += f" AND ({category_conditions})"
    
    if preferencias_dificultad:
        difficulty_conditions = " OR ".join([f"Dificultad LIKE '%{diff.strip()}%'" for diff in preferencias_dificultad])
        query += f" AND ({difficulty_conditions})"
    
    cursor.execute(query)
    recipes = cursor.fetchall()
    
    conn.close()
    return recipes
