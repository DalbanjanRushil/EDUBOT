import os
import pdfplumber
from dotenv import load_dotenv

from langchain.text_splitter import CharacterTextSplitter
from langchain_cohere import CohereEmbeddings, ChatCohere
from langchain_community.vectorstores import FAISS

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableMap, RunnableLambda

# Load environment variables
load_dotenv()
cohere_api_key = os.getenv("COHERE_API_KEY")


# Step 1: Extract text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text() or ''
        if text.strip() == '':
            print("❌ No extractable text found in the PDF.")
            exit()
        print("✅ Text extracted successfully.")
        return text
    except Exception as e:
        print("❌ Error reading PDF:", e)
        exit()


# Step 2: Split text into chunks
def split_text(text):
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    return splitter.split_text(text)


# Step 3: Create vector store
def create_vector_store(chunks):
    embeddings = CohereEmbeddings(model="embed-english-v3.0")
    vectorstore = FAISS.from_texts(chunks, embedding=embeddings)
    return vectorstore


# Step 4: Ask questions using new runnable pipeline
def ask_question(vectorstore, query):
    docs = vectorstore.similarity_search(query)
    context = "\n\n".join([doc.page_content for doc in docs])

    llm = ChatCohere(model="command-r-plus", temperature=0.3)

    prompt = PromptTemplate.from_template(
        "Answer the following question based on the context:\n\n{context}\n\nQuestion: {question}"
    )

    chain = (
        RunnableMap({"context": lambda x: context, "question": lambda x: x["question"]})
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke({"question": query})


# Run the bot
def run_bot():
    print("🔄 Reading PDF and preparing AI bot...")

    pdf_path = "data/learningbasicenglishgrammar.pdf"
    pdf_path = "data/CHAPTER 6.pdf"  # Make sure this file exists
    text = extract_text_from_pdf(pdf_path)
    chunks = split_text(text)
    vectorstore = create_vector_store(chunks)

    print("🤖 Ready! Ask any question about your PDF.")
    while True:
        query = input("👤 You: ")
        if query.lower() in ['exit', 'quit']:
            print("👋 Exiting bot. Bye!")
            break
        answer = ask_question(vectorstore, query)
        print("🤖 Bot:", answer)


if __name__ == "__main__":
    run_bot()
