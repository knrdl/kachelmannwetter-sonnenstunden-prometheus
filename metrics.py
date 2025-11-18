import requests
import time
import json

_cache_value: str | None = None
_cache_ts: int | None = None

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
    'Pragma':	'no-cache',
    'Priority': 'u=0, i',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-GPC': '1'
}
ses = requests.Session()

def generate(area_id: int, station_id: str) -> str:
    global _cache_value, _cache_ts

    now = int(time.time())

    if not _cache_ts or now - _cache_ts > 60 * 60:
        output = ''

        resp = ses.get('https://kachelmannwetter.com/de/messwerte/sonnenstunden', headers=headers)

        resp = ses.get('https://kachelmannwetter.com/de/ajax/obsdetail', headers=headers, params={
                'model': 'obs',
                'param_id': '64',
                'counter': 'false',
                'lang': 'DE',
                'station_id': station_id, 
                'timestamp': time.strftime('%Y%m%d%H00'), 
                'area_id': str(area_id),
            })

        if resp.status_code != 200:
            raise Exception(f'wrong response code={resp.status_code}; text={resp.text}; headers={resp.headers}')
        records: list[dict[str, int]] = json.loads(resp.text.split(' var hc_obs_series = ')[1].split(';')[0])[0]['data']
        for record in records:
            timestamp = record['x']
            value = record['y']
            output += f'kachelmannwetter_sonnenstunden{{area_id="{area_id}",station_id="{station_id}"}} {value} {timestamp}\n'
        
        _cache_ts = now
        _cache_value = output

    return _cache_value
