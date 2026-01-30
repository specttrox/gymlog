import pandas as pd
import sqlite3

# 1. Carregar o CSV para a memória (Extract)
# O Pandas lê o arquivo e transforma numa tabela gigante na memória RAM
df = pd.read_csv('workout_data.csv')

# Conectar ao banco (Load)
conn = sqlite3.connect('gymlog.db')
cursor = conn.cursor()

print("Iniciando a migração dos dados...")

# ---------------------------------------------------------
# ETAPA 1: Povoar a tabela de EXERCÍCIOS (Exercises)
# ---------------------------------------------------------
# Lógica: O CSV tem "Supino" repetido 1000 vezes. 
# Pegamos apenas os nomes ÚNICOS para criar nosso catálogo.
unique_exercises = df['exercise_title'].unique()

print(f"Encontrados {len(unique_exercises)} exercícios únicos.")

for exercise_name in unique_exercises:
    # INSERT OR IGNORE: Se já existir esse nome, não faz nada (evita erro)
    cursor.execute("INSERT OR IGNORE INTO exercises (name) VALUES (?)", (exercise_name,))

# Salvar (Commit) para garantir que os IDs existam para os próximos passos
conn.commit()

# ---------------------------------------------------------
# ETAPA 2: Povoar TREINOS e SÉRIES (Workouts & Sets)
# ---------------------------------------------------------
# Aqui precisamos ser espertos. Vamos ler linha por linha do CSV.
# Para cada linha, descobrimos a qual treino ela pertence e salvamos a série.

# Dicionário para memória rápida: "26 Jan 2026 16:58" -> ID do Treino no Banco
# Isso evita que a gente pergunte ao banco 1000 vezes se o treino existe.
workout_map = {} 

for index, row in df.iterrows():
    # Dados da linha atual do CSV
    data_inicio = row['start_time']
    data_fim = row['end_time']
    titulo_treino = row['title']
    nome_exercicio = row['exercise_title']
    
    # Chave única para identificar um treino: Data + Título
    treino_key = f"{data_inicio}_{titulo_treino}"

    # --- Lógica do Treino (Workout) ---
    # Se ainda não processamos esse treino, criamos ele no banco agora
    if treino_key not in workout_map:
        cursor.execute(
            "INSERT INTO workouts (title, start_time, end_time) VALUES (?, ?, ?)",
            (titulo_treino, data_inicio, data_fim)
        )
        # O banco acabou de criar um ID (ex: 1, 2, 3). Precisamos pegar esse número!
        workout_id = cursor.lastrowid
        workout_map[treino_key] = workout_id
    else:
        # Se já processamos, só recuperamos o ID da nossa memória
        workout_id = workout_map[treino_key]

    # --- Lógica do Exercício ---
    # Precisamos saber qual o ID do "Supino" no banco para vincular a série
    cursor.execute("SELECT id FROM exercises WHERE name = ?", (nome_exercicio,))
    exercise_result = cursor.fetchone()
    
    if exercise_result:
        exercise_id = exercise_result[0]
        
        # --- Inserir a Série (Set) ---
        cursor.execute("""
            INSERT INTO sets (workout_id, exercise_id, weight_kg, reps)
            VALUES (?, ?, ?, ?)
        """, (workout_id, exercise_id, row['weight_kg'], row['reps']))

conn.commit()
conn.close()
print("Sucesso! Todos os dados foram migrados para o Banco de Dados.")