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
            full_url: str = (
                self.base_url.rstrip('/')
                + '/' + endpoint.lstrip('/')
            )
            response: requests.Response = requests.get(full_url)
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


class SWRequester(APIRequester):
    def __init__(self):
        super().__init__('https://swapi.dev/api/')

    def get_sw_categories(self) -> list:
        response: Optional[requests.Response] = self.get()
        if response is None:
            logging.info('<Запрос к API не удался>')
            return []
        try:
            response_json = response.json()

        except ValueError:
            logging.info('<Не получилось закодировать в JSON>')
            return []

        except Exception as e:
            logging.info(f'Ошибка: {e}')
            return []

        return list(response_json.keys())

    def get_sw_info(self, sw_type: str) -> Optional[requests.Response]:
        available_categories: list = self.get_sw_categories()
        if sw_type in available_categories:
            endpoint: str = sw_type.lstrip('/')
            response: Optional[requests.Response] = self.get(
                endpoint.rstrip('/') + '/'
            )
            if response is None:
                logging.error('Ошибка в запросе')
            return response
        else:
            logging.error(
                f'<Этой категории - {sw_type} нет '
                'в доступных: {available_categories}>'
                )
            return None


api_swapi = SWRequester()
print(api_swapi.get_sw_categories())
