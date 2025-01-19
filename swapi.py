from pathlib import Path
from urllib.parse import urlparse, ParseResult
import requests
from typing import KeysView


def save_sw_data():
    sw_requester = SWRequester('https://swapi.dev/api')
    Path("data").mkdir(exist_ok=True)
    categories = sw_requester.get_sw_categories()
    for category in categories:
        with open(f'data/{category}.txt', 'w') as file:
            file.write(str(sw_requester.get_sw_info(category)))


class APIRequester:
    def __init__(self, base_url: str):
        parsed: ParseResult = urlparse(base_url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f'Не корректный URL: {base_url}')

        self.base_url: str = base_url

    def get(
        self,
        endpoint: str = ''
    ) -> requests.Response:
        try:
            full_url: str = (
                self.base_url.rstrip('/')
                + '/' + endpoint.lstrip('/')
            )
            response: requests.Response = requests.get(full_url, timeout=10)
            response.raise_for_status()
            return response
        except requests.TooManyRedirects:
            print('Слишком много перенаправлений.')
        except requests.URLRequired:
            print('Для отправки запроса требуется действительный URL')
        except requests.HTTPError:
            print('Ошибка на сервере')
        except requests.ConnectionError:
            print('Cетевая ошибка')
        except requests.Timeout:
            print(
                'Время ожидания запроса истекло при подключении'
                )
        except requests.Timeout:
            print('Время ожидания запроса истекло')
        except requests.RequestException:
            print(
                'Возникла ошибка при выполнении запроса'
                )
        except Exception:
            print('Ошибка в ответе')


class SWRequester(APIRequester):
    def get_sw_categories(self) -> KeysView[str]:
        response: requests.Response = self.get()
        try:
            response_json: dict = response.json()
        except requests.JSONDecodeError:
            print('<Не получилось закодировать в JSON>')
        except Exception:
            print('Не понятная ошибка')
        return response_json.keys()

    def get_sw_info(self, sw_type: str) -> str:
        endpoint: str = sw_type.lstrip('/')
        response: requests.Response = self.get(
                    endpoint.rstrip('/') + '/'
                )
        return response.text
