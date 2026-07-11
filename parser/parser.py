# непосредственно сами функции извлечения данных
import aiohttp
import asyncio
import json
from pydantic import BaseModel, ValidationError
import aiohttp
import random
from aiolimiter import AsyncLimiter
from tqdm.asyncio import tqdm

#ограничитель для acyncio
limiter = AsyncLimiter(1, time_period=4)

url = "https://pb.nalog.ru/search-proc.json"

PROXY_LIST = []

# Заголовки из curl
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://pb.nalog.ru",
    "Connection": "keep-alive",
    "Referer": "https://pb.nalog.ru/search.html",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
}
cookies = {
    "JSESSIONID": "6337B6A83E745A1D760EB6EDCDBC66FA"
    #"JSESSIONID": "FA940757EC251E0EB1E5890DE54BA529"
}

# FIXME кастомные исключения можно вынести в отдельный модуль
class NalogError(Exception):
    pass

# чисто чтобы убедиться что ид там есть
class NalogResponse(BaseModel):
    id: str


# Модель для проверки структуры ответа
class UprContainer(BaseModel):
    data: list  # внутри upr должен быть список data

class DirectorDataContainer(BaseModel):
    data: list

class DirectorDataResponse(BaseModel):
    ul: DirectorDataContainer

class NalogDataResponse(BaseModel):
    upr: UprContainer  # на верхнем уровне обязательное поле upr
    #FIXME а может сделать один класс вместо двух?

async def fetch_nalog_id(query:str) -> str:
    data = {
        "mode": "search-upr-uchr",
        "queryAll": query,
        "queryUl": "",
        "okvedUl": "",
        "okvedTypeUl": "",
        "regionUl": "",
        "statusUl": "",
        "isMspUl": "",
        "mspUl1": "1",
        "mspUl2": "1",
        "mspUl3": "1",
        "queryIp": query,
        "okvedIp": "",
        "okvedTypeIp": "",
        "regionIp": "",
        "statusIp": "",
        "isMspIp": "",
        "mspIp1": "1",
        "mspIp2": "1",
        "mspIp3": "1",
        "taxIp": "",
        "queryUpr": query,
        "uprType1": "1",
        "queryRdl": "",
        "dateRdl": "",
        "queryAddr": "",
        "regionAddr": "",
        "queryOgr": "",
        "ogrFl": "1",
        "ogrUl": "1",
        "ogrnUlDoc": "",
        "ogrnIpDoc": "",
        "npTypeDoc": "1",
        "nameUlDoc": "",
        "nameIpDoc": "",
        "formUlDoc": "",
        "formIpDoc": "",
        "ifnsDoc": "",
        "dateFromDoc": "",
        "dateToDoc": "",
        "page": "1",
        "pageSize": "100",
        "pbCaptchaToken": "",
        "token": ""
    }
    async with aiohttp.ClientSession(headers=headers, cookies=cookies, proxy=random.choice(PROXY_LIST) if len(PROXY_LIST) else None) as session:
        async with limiter:
            async with session.post(url, data=data) as response:
                if response.status != 200:
                    raise RuntimeError(f"HTTP {response.status}: {await response.text()}")
                try:
                    raw = await response.json()
                    validated = NalogResponse.model_validate(raw)
                    return validated.id
                except (aiohttp.ContentTypeError, ValueError, ValidationError) as e:
                    raise RuntimeError("Не удалось распарсить или валидировать ответ") from e
            

async def fetch_director_data_id(token: str, name: str) -> str:
    data_payload = {
        'mode': 'search-ul',
        'queryAll': '',
        'queryUl': name,
        'okvedUl': '',
        'okvedTypeUl': '',
        'regionUl': '',
        'statusUl': '',
        'isMspUl': '',
        'mspUl1': '1',
        'mspUl2': '1',
        'mspUl3': '1',
        'queryIp': '',
        'okvedIp': '',
        'okvedTypeIp': '',
        'regionIp': '',
        'statusIp': '',
        'isMspIp': '',
        'mspIp1': '1',
        'mspIp2': '1',
        'mspIp3': '1',
        'taxIp': '',
        'queryUpr': '',
        'uprType1': '1',
        'queryRdl': '',
        'dateRdl': '',
        'queryAddr': '',
        'regionAddr': '',
        'queryOgr': '',
        'ogrFl': '1',
        'ogrUl': '1',
        'ogrnUlDoc': '',
        'ogrnIpDoc': '',
        'npTypeDoc': '1',
        'nameUlDoc': '',
        'nameIpDoc': '',
        'formUlDoc': '',
        'formIpDoc': '',
        'ifnsDoc': '',
        'dateFromDoc': '',
        'dateToDoc': '',
        'page': '1',
        'pageSize': '100',
        'pbCaptchaToken': '',
        'token': token
    }
    async with aiohttp.ClientSession(headers=headers, cookies=cookies, proxy=random.choice(PROXY_LIST) if len(PROXY_LIST) else None) as session:
        async with limiter:
            async with session.post(url, data=data_payload) as response:
                # Проверка статуса
                if response.status != 200:
                    error_text = await response.text()
                    raise NalogError(f"HTTP {response.status}: {error_text[:200]}")
                try:
                    raw = await response.json()
                    validated = NalogResponse.model_validate(raw)
                    return validated.id
                except (aiohttp.ContentTypeError, ValueError, ValidationError) as e:
                    raise NalogError("Не удалось распарсить или валидировать ответ") from e
            
async def fetch_director_data(id: str) -> list:
    """
    Получает данные по ID и возвращает список из поля upr.data.
    """
    data_payload = {
        "id": id,
        "method": "get-response"
    }
    async with aiohttp.ClientSession(headers=headers, cookies=cookies, proxy=random.choice(PROXY_LIST) if len(PROXY_LIST) else None) as session:
        async with limiter:
            async with session.post(url, data=data_payload) as response:
                # Проверка статуса
                if response.status != 200:
                    error_text = await response.text()
                    raise NalogError(f"HTTP {response.status}: {error_text[:200]}")

                try:
                    raw = await response.json()
                    #print(raw)
                except (aiohttp.ContentTypeError, ValueError) as e:
                    raise NalogError("Ответ сервера не является корректным JSON") from e

                # валидация через Pydantic
                try:
                    validated = DirectorDataResponse.model_validate(raw)
                except ValidationError as e:
                    raise NalogError(f"Неверная структура ответа: {e}") from e

                return validated.ul.data
        
async def fetch_nalog_data(id: str) -> list:
    """
    Получает данные по ID и возвращает список из поля upr.data.
    """
    data_payload = {
        "id": id,
        "method": "get-response"
    }
    async with aiohttp.ClientSession(headers=headers, cookies=cookies, proxy=random.choice(PROXY_LIST) if len(PROXY_LIST) else None) as session:
        async with limiter:
            async with session.post(url, data=data_payload) as response:
                # Проверка статуса
                if response.status != 200:
                    error_text = await response.text()
                    raise NalogError(f"HTTP {response.status}: {error_text[:200]}")

                try:
                    raw = await response.json()
                except (aiohttp.ContentTypeError, ValueError) as e:
                    raise NalogError("Ответ сервера не является корректным JSON") from e

                # валидация через Pydantic
                try:
                    validated = NalogDataResponse.model_validate(raw)
                except ValidationError as e:
                    raise NalogError(f"Неверная структура ответа: {e}") from e

                # FIXME возвращать ли сразу список?
                return validated.upr.data
        
async def fetch(query: str):
    id = await fetch_nalog_id("Андрей")
    data = await fetch_nalog_data(id)

    # Прогресс-бар для цикла по людям
    for person in tqdm(data, desc="Обработка людей"):
        person_id = await fetch_director_data_id(person['token'], person['name'])
        # организации, в которых этот перс директор
        person['orgs'] = await fetch_director_data(person_id)

    return data

if __name__ == "__main__":
    data = asyncio.run(fetch("Андрей"))