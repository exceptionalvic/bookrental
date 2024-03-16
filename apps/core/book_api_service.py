import requests

def fetch_book_details(title):
    response = requests.get(f"https://openlibrary.org/search.json?q={str(title).replace(' ','+').lower()}&limit=1")
    data = response.json()
    if 'docs' in data and data['docs']:
        book_data = data['docs'][0]
        # print(book_data)
        return {
            'title': book_data.get('title', ''),
            'author': book_data.get('author_name', [''])[0],
            'number_of_pages': book_data.get('number_of_pages', book_data.get('number_of_pages_median', 0))
        }
    return None