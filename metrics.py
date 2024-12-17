from urllib.request import urlopen
from urllib.parse import urlencode
import time
import json

_cache_value: str | None = None
_cache_ts: int | None = None

def generate(area_id: int, station_id: int) -> str:
    global _cache_value, _cache_ts

    now = int(time.time())

    if not _cache_ts or now - _cache_ts > 60 * 60:
        _cache_ts = now

        output = ''
        resp = urlopen('https://kachelmannwetter.com/de/ajax/obsdetail?' + urlencode({
            'model': 'obs',
            'param_id': '64',
            'counter': 'false',
            'lang': 'DE',
            'station_id': str(station_id), 
            'timestamp': time.strftime('%Y%m%d%H00'), 
            'area_id': str(area_id)
        }))
        if resp.code != 200:
            raise Exception(f'wrong response code: {resp.code}')
        records: list[dict[str, int]] = json.loads(resp.read().decode().split(' var hc_obs_series = ')[1].split(';')[0])[0]['data']
        for record in records:
            timestamp = record['x']
            value = record['y']
            output += f'kachelmannwetter_sonnenstunden{{area_id="{area_id}",station_id="{station_id}"}} {value} {timestamp}\n'
        
        _cache_value = output

    return _cache_value
