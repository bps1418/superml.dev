from fastapi import FastAPI, Request
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, Tool
from langchain.tools import tool
from langchain.prompts.chat import ChatPromptTemplate
from langchain.output_parsers import StrOutputParser

app = FastAPI()
llm = ChatOpenAI(temperature=0, model="gpt-4")

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Tool definitions
@tool
def calculator(input: str) -> str:
    try:
        return str(eval(input))
    except Exception:
        return "Error in calculation"

@tool
def fake_search(query: str) -> str:
    return f"Simulated result for: {query}"

tools = [Tool(name="Calculator", func=calculator, description="Useful for math"),
         Tool(name="Search", func=fake_search, description="Useful for current events")]

# Prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}")
])

# Output parser
parser = StrOutputParser()

# Vector store setup
retriever = None
try:
    vectorstore = FAISS.load_local("faiss_index", OpenAIEmbeddings())
    retriever = vectorstore.as_retriever()
except Exception:
    print("Vectorstore not found, skipping RetrievalQAChain.")

# Agent
agent = initialize_agent(tools, llm, agent="chat-conversational-react-description", memory=memory)

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_input = body.get("input", "")
    result = agent.run(user_input)
    return {"response": result}
