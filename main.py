import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from ai_agent import agent_executor

app = FastAPI(title="gymlog")

# define modelo de dados para resposta
class WorkoutSchema(BaseModel):
    id: int
    title: str
    start_time: str
    end_time: str

# conecta ao banco sqlite
def get_db_connection():
    conn = sqlite3.connect("gymlog.db")
    conn.row_factory = sqlite3.Row 
    return conn

# rota para listar todos os treinos
@app.get("/treinos", response_model=List[WorkoutSchema])
def listar_treinos():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # busca tudo na tabela workouts
    cursor.execute("SELECT * FROM workouts")
    treinos = cursor.fetchall()
    
    conn.close()
    return [dict(row) for row in treinos]

# rota para buscar treino unico por id
@app.get("/treinos/{treino_id}")
def pegar_treino_especifico(treino_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # consulta segura usando parametro
    cursor.execute("SELECT * FROM workouts WHERE id = ?", (treino_id,))
    treino = cursor.fetchone()
    
    conn.close()
    
    if treino is None:
        return {"erro": "treino nao encontrado"}
    
    return dict(treino)

# Rota da IA
class PerguntaSchema(BaseModel):
    texto: str

@app.post("/ask")
def perguntar_ia(pergunta: PerguntaSchema):
    # manda a pergunta
    resposta = agent_executor.invoke(pergunta.texto)
    
    # retorna resposta final
    return {"resposta": resposta["output"]}