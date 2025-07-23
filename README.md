# kachelmannwetter-sonnenstunden-prometheus

https://kachelmannwetter.com/de/messwerte/berlin/sonnenstunden/20241217-0600z.html#obs-detail-103850

https://kachelmannwetter.com/de/ajax/obsdetail?station_id=103850&timestamp=202412170600&param_id=64&model=obs&area_id=39&counter=false&lang=DE


```yaml
services:
  kachelmannwetter-sonnenstunden:
    image: ghcr.io/knrdl/kachelmannwetter-sonnenstunden-prometheus:edge
    restart: always
    environment:
      area_id: '39'
      station_id: '103850'
    mem_limit: 100m
    ports:
      - 8080:8080
```