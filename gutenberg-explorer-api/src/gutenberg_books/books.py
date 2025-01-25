from requests import get
from fastapi import FastAPI, status, Response
from src.model.const import GUTENBERG_BASE_URL, GUTENBERG_BOOK_ID_PATH, GUTENBERG_BOOK_METADATA_PATH
from src.gutenberg_books.parse_html_doc_to_model import parse_html_to_model
from bs4 import BeautifulSoup

book_sub_app = FastAPI()

@book_sub_app.get("/{book_id}", status_code=200)
async def get_book_meta(book_id: str, response: Response):
    '''
    Extract Metadata From Gutenberg
    '''
    try:
        url = f"{GUTENBERG_BASE_URL}/{GUTENBERG_BOOK_METADATA_PATH}/{book_id}"
        res = get(url, timeout=10000)

        if res.status_code == 200:
            document = BeautifulSoup(response.content, "html.parser")
            book = parse_html_to_model(document)
            return {"data": book}
        elif res.status_code == 404:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "Book not found"}
        else:
            raise RuntimeError("Unhandled Exception")
    except RuntimeError as _:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "Something went wrong"}


@book_sub_app.get("/content/{book_id}", status_code=200)
def get_book_text(book_id: str, response: Response):
    '''
    Extract Book Content From Gutenberg
    '''
    try:
        url = f"{GUTENBERG_BASE_URL}/{GUTENBERG_BOOK_ID_PATH}/{book_id}/{book_id}-0.txt"
        res = get(url, timeout=10000)

        if res.status_code == 200:
            parsed_content = res.content
            return {"data": parsed_content}
        elif res.status_code == 404:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "Book not found"}
        else:
            raise RuntimeError("Unhandled Exception")
    except RuntimeError as _:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "Something went wrong"}
