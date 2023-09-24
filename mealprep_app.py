import re
import csv
import random
from database_manager import get_available_recipes, add_to_history, get_all_recipes, get_filtered_recipes

class MealPrepApp:
    def __init__(self):
        pass

    def get_weekly_plan(self, comidas_por_dia, num_dias, preferencia_categoria="", preferencia_dificultad=""):
        total_comidas = comidas_por_dia * num_dias
        
        # Filtrar recetas basadas en las preferencias del usuario
        available_recipes = get_filtered_recipes(preferencia_categoria, preferencia_dificultad)
        
        # Si no hay suficientes recetas disponibles, repetimos algunas al azar
        while len(available_recipes) < total_comidas:
            available_recipes += available_recipes
            
        weekly_plan = random.sample(available_recipes, total_comidas)
        
        for recipe in weekly_plan:
            add_to_history(recipe[0])
            
        return weekly_plan

    def get_shopping_list(self, weekly_plan, num_personas=2):
        ingredients = []
        for recipe in weekly_plan:
            for ingredient in recipe[-1].split(','):
                match = re.match(r'(\d+)', ingredient.strip())
                if match and recipe[5]:  # Verificar si hay un número de comensales especificado
                    quantity = int(match.group(1))
                    adjusted_quantity = (quantity * num_personas) // int(recipe[5])
                    ingredient = ingredient.replace(str(quantity), str(adjusted_quantity), 1)
                ingredients.append(ingredient)
        
        # Aquí puedes agregar lógica para combinar ingredientes similares si es necesario
        
        return ingredients

    def export_to_csv(self, data, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerows(data)
