from database_manager import create_database, upload_csv_to_db, clear_history, get_unique_values
from mealprep_app import MealPrepApp

def main():
    app = MealPrepApp()
    
    # Supongamos que quieres cargar un CSV y obtener un plan semanal
    #upload_csv_to_db('recetas.csv')
    
    # Preguntar al usuario sobre sus preferencias de categoría
    categorias = get_unique_values('Categoria')
    print("Categorías disponibles:", ", ".join(categorias))
    preferencias_categoria = input("¿Qué tipos de comidas prefieres? (Separa con comas, p.ej. 'pescado, carne'): ").lower().split(',')
    
    # Preguntar al usuario sobre su preferencia de dificultad
    dificultades = get_unique_values('Dificultad')
    print("Dificultades disponibles:", ", ".join(dificultades))
    preferencias_dificultad = input("¿Qué niveles de dificultad prefieres? (Separa con comas, p.ej. 'fácil, medio'): ").lower().split(',')
    
    # Pregunta al usuario el número de personas, comidas por día y días
    num_personas = int(input("¿Para cuántas personas es el plan? "))
    comidas_por_dia = int(input("¿Cuántas comidas al día por persona? "))
    num_dias = int(input("¿Para cuántos días es el plan? "))
    
    weekly_plan = app.get_weekly_plan(comidas_por_dia, num_dias, preferencias_categoria, preferencias_dificultad)
    app.export_to_csv(weekly_plan, 'weekly_plan.csv')
    
    # Obtener lista de la compra y exportarla
    shopping_list = app.get_shopping_list(weekly_plan, num_personas)
    app.export_to_csv([(item,) for item in shopping_list], 'shopping_list.csv')

if __name__ == "__main__":
    create_database()
    main()
