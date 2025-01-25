import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.gutenberg_books.books import book_sub_app

main_app = FastAPI()

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

main_app.mount(path="/book", app=book_sub_app)

if __name__ == "__main__":
    uvicorn.run(main_app, host="127.0.0.1", port=8000)