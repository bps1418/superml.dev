# LangChain Chat Application

A simple chat API built with FastAPI and LangChain that integrates:

- Prompt Templates
- Agents
- Tools (Calculator, Search)
- Memory
- Output Parsers
- Vector Store (FAISS)

## Run the API

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Endpoint

POST `/chat` with payload: `{"input": "your message here"}`

## Example

```bash
curl -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d '{"input": "2+2"}'
```
