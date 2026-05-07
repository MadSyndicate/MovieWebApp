import os
import requests

DATA_URL = "https://www.omdbapi.com"
API_KEY = os.getenv('API_KEY')


def fetch_movie_data(title):
    """"""
    params = {
        "apikey": API_KEY,
        "t": title
    }
    try:
        res = requests.get(DATA_URL, params=params, timeout=5)  # 5sec timeout
        return res.json()
    except requests.exceptions.HTTPError:
        print('HTTP Error')
        return None
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
        print('TIMEOUT Error')
        return None
