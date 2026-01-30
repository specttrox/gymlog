import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

# carrega a chave
load_dotenv()

# pega a chave
chave_groq = os.getenv("GROQ_API_KEY")

# conecta ao banco
db = SQLDatabase.from_uri("sqlite:///gymlog.db")

# configura o modelo
llm = ChatGroq(
    groq_api_key=chave_groq, 
    model_name="llama-3.3-70b-versatile"
)

# cria o agente
agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    agent_type="openai-tools",
    verbose=True,
    handle_parsing_errors=True
)