# app.py

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import main as bot_module

app = FastAPI()

# Load PDF + create vectorstore once
text = bot_module.extract_text_from_pdf("data/CHAPTER 6.pdf")
chunks = bot_module.split_text(text)
vectorstore = bot_module.create_vector_store(chunks)


@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
    <head>
        <title>EduBot PDF Chat 🤖</title>
        <style>
            body { font-family: sans-serif; max-width: 700px; margin: 40px auto; padding: 20px; }
            input, button, textarea { width: 100%; padding: 10px; margin-top: 10px; }
            #answer { white-space: pre-wrap; background: #f5f5f5; padding: 15px; margin-top: 10px; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h2>🤖 Ask a Question About the PDF</h2>
        <form action="/" method="post">
            <input type="text" name="query" placeholder="e.g. What is a noun?" required />
            <button type="submit">Ask</button>
        </form>
        {answer}
    </body>
    </html>
    """.replace("{answer}", "")

@app.post("/", response_class=HTMLResponse)
async def get_answer(query: str = Form(...)):
    answer = bot_module.ask_question(vectorstore, query)
    return f"""
    <html>
    <head>
        <title>EduBot PDF Chat 🤖</title>
        <style>
            body {{ font-family: sans-serif; max-width: 700px; margin: 40px auto; padding: 20px; }}
            input, button, textarea {{ width: 100%; padding: 10px; margin-top: 10px; }}
            #answer {{ white-space: pre-wrap; background: #f5f5f5; padding: 15px; margin-top: 10px; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <h2>🤖 Ask a Question About the PDF</h2>
        <form action="/" method="post">
            <input type="text" name="query" placeholder="e.g. What is a noun?" required />
            <button type="submit">Ask</button>
        </form>
        <div id="answer"><strong>Answer:</strong><br>{answer}</div>
    </body>
    </html>
    """
