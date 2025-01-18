import logging
import requests
from typing import Optional
from urllib.parse import urlparse, ParseResult


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class APIRequester:
    def __init__(self, base_url: str):
        parsed: ParseResult = urlparse(base_url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f'Не корректный URL: {base_url}')

        self.base_url = base_url

    def get(
        self,
        endpoint: str = ''
    ) -> Optional[requests.Response]:
        try:
            full_url = self.base_url.rstrip('/') + '/' + endpoint.lstrip('/')
            response = requests.get(full_url)
            response.raise_for_status()

        except requests.HTTPError as e:
            logging.error(f'<Ошибка на сервере: {e}>')
            return None

        except requests.ConnectionError as e:
            logging.error(f'<Cетевая ошибка: {e}>')
            return None

        except requests.ConnectTimeout as e:
            logging.error(
                f'<Время ожидания запроса истекло при подключении: {e}>'
                )
            return None

        except requests.Timeout as e:
            logging.info(f'<Время ожидания запроса истекло: {e}>')
            return None

        except Exception as e:
            logging.info(f'<Ошибка в ответе: {e}>')
            return None

        else:
            logging.info('<Получен успешный ответ>')
            return response


URL = 'https://swapi.dev/api/people/'
api_swapi = APIRequester(URL)
print(api_swapi.get())
