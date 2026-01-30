# Gymlog

API desenvolvida para análise de dados de treinos de musculação utilizando Inteligência Artificial (LLM).

## Motivação

Utilizo o aplicativo "Hevy" (iOS) para registrar meus treinos. O app é excelente, mas as estatísticas avançadas e o histórico completo são restritos à assinatura paga.

Como eu tinha acesso aos meus dados brutos (exportação CSV) e queria aprender mais sobre Python e Engenharia de Dados, decidi criar minha própria solução caseira. Em vez de pagar para ver gráficos prontos, preferi construir um sistema onde eu pudesse perguntar qualquer coisa sobre meus treinos.

## Processo de Desenvolvimento

Esse projeto foi um teste real pra ver como é programar com ajuda de LLMs hoje em dia, usando tanto para tirar dúvidas teóricas quanto para partes específicas do código. Usei a versão gratuita do Gemini para me ajudar a entender a API da Groq, o que adiantou bastante o lado.

Mas uma coisa é óbvia (e a depender do contexto, pode mais atrapalhar do que ajudar): não dá pra confiar cegamente. Várias vezes a IA sugeriu coisas desconexas, perdeu o contexto ou inventou parâmetros no FastAPI que davam erro na hora de rodar. Tive que ir atrás de documentação oficial e pesquisar no Google pra corrigir e fazer funcionar de verdade. Algumas comunidades do Reddit ajudaram bastante também.

O mais legal foi implementar e observar a ideia de "Agentes". Na prática, a IA serve como um tradutor: ela pega o que eu falo em português, transforma em comandos técnicos (SQL), executa no banco e me devolve a resposta. É a mesma lógica que grandes empresas (como Apple e Google) estão tentando colocar nos celulares: a IA abstrai a parte técnica e chata, e simplesmente usa as ferramentas disponíveis para entregar o que o usuário pediu.

## Como funciona

O projeto segue um fluxo de dados simples:

1. **Extração:** Exportação dos dados brutos do app Hevy em formato CSV.
2. **ETL (Extract, Transform, Load):** Script em Python (`pandas`) que limpa os dados, trata tipos e normaliza as tabelas.
3. **Armazenamento:** Os dados tratados são migrados para um banco de dados relacional SQLite.
4. **API:** Back-end desenvolvido com FastAPI para expor os dados.
5. **Inteligência Artificial:** Integração com a API da Groq (Modelo Llama 3) via LangChain. O agente converte perguntas em português para queries SQL e interpreta os resultados.

## Tecnologias

- **Linguagem:** Python 3.12
- **API:** FastAPI, Uvicorn
- **Banco de Dados:** SQLite, SQLAlchemy
- **Dados:** Pandas (para manipulação do CSV)
- **IA/LLM:** LangChain, Groq API

## Estrutura do Projeto

- `etl.py`: Script responsável por ler o CSV e popular o banco de dados.
- `database.py`: Configuração da conexão com o SQLite.
- `main.py`: A aplicação principal (API) e rotas.
- `ai_agent.py`: Configuração do agente de IA e conexão com o modelo Llama.
- `requirements.txt`: Lista de dependências do projeto.
