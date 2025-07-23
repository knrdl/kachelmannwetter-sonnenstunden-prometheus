import requests
import time
import json

_cache_value: str | None = None
_cache_ts: int | None = None

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}
ses = requests.Session()

def generate(area_id: int, station_id: str) -> str:
    global _cache_value, _cache_ts

    now = int(time.time())

    if not _cache_ts or now - _cache_ts > 60 * 60:
        _cache_ts = now

        output = ''

        resp = ses.get('https://kachelmannwetter.com/de/messwerte/stadt-berlin/sonnenstunden/20250723-0600z.html', headers=headers)

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
            raise Exception(f'wrong response code: {resp.status_code}')
        records: list[dict[str, int]] = json.loads(resp.text.split(' var hc_obs_series = ')[1].split(';')[0])[0]['data']
        for record in records:
            timestamp = record['x']
            value = record['y']
            output += f'kachelmannwetter_sonnenstunden{{area_id="{area_id}",station_id="{station_id}"}} {value} {timestamp}\n'
        
        _cache_value = output

    return _cache_value
