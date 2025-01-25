from bs4 import BeautifulSoup
from src.util.string_util import snake_case

def parse_html_to_model(document: BeautifulSoup):
    '''
    Parse Metadata From HTML
    '''
    metadata_gutenberg_known_keys = {
        "author",
        "title",
        "original_publication",
        "credits",
        "language",
        "category",
        "ebook_number",
        "release_date",
        "downloads"
    }

    book_metadata: dict = {}
    metadata_table_class = 'bibrec'
    metadata_cover_image_class = 'cover-art'

    metadata_table = document.find('table', class_=metadata_table_class)
    image_node = document.find('img', class_=metadata_cover_image_class)
    image_source = image_node['src'] if image_node else None

    if image_source:
        book_metadata["cover_url"] = image_source

    for row in metadata_table.find_all('tr'):
        key = row.find('th')
        value = row.find('td')
        if not key or not value:
            continue

        parsed_key = snake_case(key.text.strip())

        if parsed_key not in metadata_gutenberg_known_keys:
            continue

        book_metadata[parsed_key] = value.text.strip()

    return book_metadata
