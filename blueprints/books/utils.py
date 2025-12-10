import requests


def search_google_books(query: str):
    url = 'https://www.googleapis.com/books/v1/volumes'
    params = {'q': query, 'maxResults': 10}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get('items', [])
    except requests.RequestException:
        return []