import pandas as pd
import sqlite3

df = pd.read_csv('workout_data.csv')

conn = sqlite3.connect('gymlog.db')
cursor = conn.cursor()

print("Iniciando a migração dos dados...")

unique_exercises = df['exercise_title'].unique()

print(f"Encontrados {len(unique_exercises)} exercícios únicos.")

for exercise_name in unique_exercises:
    cursor.execute("INSERT OR IGNORE INTO exercises (name) VALUES (?)", (exercise_name,))

conn.commit()

workout_map = {} 

for index, row in df.iterrows():
    data_inicio = row['start_time']
    data_fim = row['end_time']
    titulo_treino = row['title']
    nome_exercicio = row['exercise_title']
    
    treino_key = f"{data_inicio}_{titulo_treino}"

    if treino_key not in workout_map:
        cursor.execute(
            "INSERT INTO workouts (title, start_time, end_time) VALUES (?, ?, ?)",
            (titulo_treino, data_inicio, data_fim)
        )
        workout_id = cursor.lastrowid
        workout_map[treino_key] = workout_id
    else:
        workout_id = workout_map[treino_key]

    cursor.execute("SELECT id FROM exercises WHERE name = ?", (nome_exercicio,))
    exercise_result = cursor.fetchone()
    
    if exercise_result:
        exercise_id = exercise_result[0]
        
        cursor.execute("""
            INSERT INTO sets (workout_id, exercise_id, weight_kg, reps)
            VALUES (?, ?, ?, ?)
        """, (workout_id, exercise_id, row['weight_kg'], row['reps']))

conn.commit()
conn.close()
print("Sucesso! Todos os dados foram migrados para o Banco de Dados.")