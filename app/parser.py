# непосредственно сами функции извлечения данных
import aiohttp
import asyncio
import json
url = "https://pb.nalog.ru/search-proc.json"

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
}
data = {
    "mode": "search-upr-uchr",
    "queryAll": "Андрей",
    "queryUl": "",
    "okvedUl": "",
    "okvedTypeUl": "",
    "regionUl": "",
    "statusUl": "",
    "isMspUl": "",
    "mspUl1": "1",
    "mspUl2": "1",
    "mspUl3": "1",
    "queryIp": "Андрей",
    "okvedIp": "",
    "okvedTypeIp": "",
    "regionIp": "",
    "statusIp": "",
    "isMspIp": "",
    "mspIp1": "1",
    "mspIp2": "1",
    "mspIp3": "1",
    "taxIp": "",
    "queryUpr": "Андрей",
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
    "page": "3",
    "pageSize": "10",
    "pbCaptchaToken": "",
    "token": ""
}

async def fetch_nalog():
    async with aiohttp.ClientSession(headers=headers, cookies=cookies) as session:
        async with session.post(url, data=data) as response:
            text = await response.text()
            print("Статус:", response.status)
            print("Ответ (первые 500 символов):", text[:500])
            try:
                return json.loads(text)["id"]
            except:
                raise RuntimeError("нет id")


if __name__ == "__main__":
    a = asyncio.run(fetch_nalog())
    print(a)