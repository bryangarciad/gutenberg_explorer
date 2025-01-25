import uvicorn
import os
import openai
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.gutenberg_books.books import book_sub_app
from src.text_interpretation.text_interpretation import analyze_text_sub_app

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

main_app = FastAPI()

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

main_app.mount(path="/book", app=book_sub_app)
main_app.mount(path="/analyze", app=analyze_text_sub_app)

if __name__ == "__main__":
    uvicorn.run(main_app, host="0.0.0.0", port=8000)
