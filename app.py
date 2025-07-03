from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import main as bot_module

app = FastAPI()

# Load PDF and create vectorstore once
text = bot_module.extract_text_from_pdf("data/CHAPTER 6.pdf")
chunks = bot_module.split_text(text)
vectorstore = bot_module.create_vector_store(chunks)

# Base Styles for Modern UI
base_styles = """
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(to right, #2b5876, #4e4376);
            color: #fff;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-attachment: fixed;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 30px;
            width: 90%;
            max-width: 500px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }
        h2 {
            text-align: center;
            font-size: 24px;
            margin-bottom: 20px;
        }
        input[type="text"], button {
            width: 100%;
            padding: 14px;
            margin-top: 10px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
        }
        input[type="text"] {
            background: #fff;
            color: #333;
        }
        button {
            background: linear-gradient(to right, #667eea, #764ba2);
            color: white;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        button:hover {
            background: linear-gradient(to right, #764ba2, #667eea);
        }
        #answer {
            margin-top: 20px;
            padding: 15px;
            background: rgba(255, 255, 255, 0.15);
            border-radius: 10px;
            white-space: pre-wrap;
            color: #fff;
        }
        .bot-icon {
            display: flex;
            justify-content: center;
            margin-bottom: 15px;
        }
        .bot-icon img {
            width: 60px;
            animation: float 3s ease-in-out infinite;
        }
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }
        @media (max-width: 600px) {
            h2 { font-size: 20px; }
            .container { padding: 20px; }
        }
    </style>
"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return f"""
    <html>
    <head>
        <title>EduBot PDF Chat 🤖</title>
        {base_styles}
    </head>
    <body>
        <div class="container">
            <div class="bot-icon">
                <img src="https://cdn-icons-png.flaticon.com/512/4712/4712035.png" alt="Bot">
            </div>
            <h2>EduBot – Ask PDF-Based Questions</h2>
            <form action="/" method="post">
                <input type="text" name="query" placeholder="e.g. What is a noun?" required />
                <button type="submit">Ask</button>
            </form>
        </div>
    </body>
    </html>
    """

@app.post("/", response_class=HTMLResponse)
async def get_answer(query: str = Form(...)):
    answer = bot_module.ask_question(vectorstore, query)
    return f"""
    <html>
    <head>
        <title>EduBot PDF Chat 🤖</title>
        {base_styles}
    </head>
    <body>
        <div class="container">
            <div class="bot-icon">
                <img src="https://cdn-icons-png.flaticon.com/512/4712/4712035.png" alt="Bot">
            </div>
            <h2>EduBot – Ask PDF-Based Questions</h2>
            <form action="/" method="post">
                <input type="text" name="query" placeholder="e.g. What is a constructor?" required />
                <button type="submit">Ask</button>
            </form>
            <div id="answer"><strong>Answer:</strong><br>{answer}</div>
        </div>
    </body>
    </html>
    """
