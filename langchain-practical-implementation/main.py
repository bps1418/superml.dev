from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents.agent_types import AgentType
from tools.search_tool import search_tool
from tools.calculator_tool import calculator_tool
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
import os

# Load environment variables
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Setup memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Load documents into vector DB
loader = TextLoader("docs/sample.txt")
docs = loader.load()
db = FAISS.from_documents(docs, OpenAIEmbeddings())
retriever = db.as_retriever()

# Setup tools
tools = [search_tool, calculator_tool]

# Setup prompt
system_template = open("system_prompt.txt").read()
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{input}")
])

# LLM setup
llm = ChatOpenAI(temperature=0, model="gpt-4")

# Agent setup
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    memory=memory
)

# Run loop
if __name__ == "__main__":
    print("LangChain Practical Chat App")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = agent.run(user_input)
        print("Assistant:", response)