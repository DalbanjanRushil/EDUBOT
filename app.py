# app.py

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import main as bot_module  # ✅ This imports your full bot code

app = FastAPI()

# ✅ Load PDF and create vector store only once
text = bot_module.extract_text_from_pdf("data/CHAPTER 6.pdf")
chunks = bot_module.split_text(text)
vectorstore = bot_module.create_vector_store(chunks)


class Question(BaseModel):
    query: str


@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <h2>🤖 Welcome to PDF Chat Bot</h2>
    <p>Send a POST request to <code>/ask</code> with JSON:</p>
    <pre>
POST /ask
{
  "query": "What is noun?"
}
    </pre>
    """


@app.post("/ask")
async def ask(q: Question):
    try:
        # ✅ Call your main.py function
        answer = bot_module.ask_question(vectorstore, q.query)
        return JSONResponse(content={"answer": answer})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
