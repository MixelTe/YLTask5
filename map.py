import requests


def getCoords(geocode):
    geocoder_request = f"https://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": geocode,
        "format": "json",
    }

    response = requests.get(geocoder_request, params=params)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_coodrinates = list(map(float, toponym_coodrinates.split(" ")))
        return toponym_coodrinates
    else:
        return None


def getMapUrlByGeocode(geocode):
    ll = getCoords(geocode)
    if (not ll):
        return None

    map_request = f"http://static-maps.yandex.ru/1.x/?ll={ll[0]},{ll[1]}&l=sat&z=13"

    return map_request
