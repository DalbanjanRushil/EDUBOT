# app.py

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import uvicorn
import threading

# Import functions from your main.py
import main as bot_module

app = FastAPI(title="LangChain PDF Bot API")

# Load PDF data once at startup
text = bot_module.extract_text_from_pdf("data/CHAPTER 6.pdf")
chunks = bot_module.split_text(text)
vectorstore = bot_module.create_vector_store(chunks)

# Define request model
class Question(BaseModel):
    query: str


@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head><title>PDF Chat Bot</title></head>
        <body>
            <h1>🤖 Welcome to PDF Chat Bot</h1>
            <p>Send a POST request to <code>/ask</code> with a question.</p>
            <p>Example:</p>
            <pre>
POST /ask
{
  "query": "What is noun?"
}
            </pre>
        </body>
    </html>
    """


@app.post("/ask")
async def ask_bot(q: Question):
    try:
        response = bot_module.ask_question(vectorstore, q.query)
        return JSONResponse(content={"answer": response})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    # Run FastAPI server in threaded mode
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
