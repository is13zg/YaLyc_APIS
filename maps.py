# coding:utf-8
import requests
import sys
import os
from io import BytesIO
from PIL import Image
import math


def get_toponim(name):
    if not name:
        return None

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": name,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    # print(response)

    if not response:
        return -2

    # Преобразуем ответ в json-объект
    json_response = response.json()
    if not (len(json_response["response"]["GeoObjectCollection"]["featureMember"])):
        return -1
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    return toponym


def get_coords(name):
    toponym = get_toponim(name)
    if type(toponym) == int:
        return toponym

    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    return ",".join([toponym_longitude, toponym_lattitude])


def get_span(name):
    toponym = get_toponim(name)
    if toponym is None:
        return (None, None)

    # Рамка вокруг объекта:
    envelope = toponym["boundedBy"]["Envelope"]

    # левая, нижняя, правая и верхняя границы из координат углов:
    l, b = envelope["lowerCorner"].split(" ")
    r, t = envelope["upperCorner"].split(" ")

    # Вычисляем полуразмеры по вертикали и горизонтали
    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0

    # Собираем размеры в параметр span
    span = f"{dx},{dy}"

    return span


def show_map(add_params=None):
    map_serv = "http://static-maps.yandex.ru/1.x/"

    map_params = {
        "ll": ",".join(["49.129465", "55.782"]),
        "spn": ",".join(["0.005", "0.005"]),
        "l": "map"
    }
    if add_params:
        map_params.update(add_params)

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    # ... и выполняем запрос
    response = requests.get(map_serv, params=map_params)

    Image.open(BytesIO(
        response.content)).show()


def bytes_map(add_params=None):
    map_serv = "http://static-maps.yandex.ru/1.x/"

    map_params = {
        "ll": ",".join(["49.129465", "55.782"]),
        #        "spn": ",".join(["0.005", "0.005"]),
        "z": 16,
        "l": "map"
    }
    if add_params:
        map_params.update(add_params)

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    # ... и выполняем запрос
    response = requests.get(map_serv, params=map_params)

    return response.content


# Определяем функцию, считающую расстояние между двумя точками, заданными координатами
def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
    a_lon, a_lat = a
    b_lon, b_lat = b

    # Берем среднюю по широте точку и считаем коэффициент для нее.
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    # Вычисляем смещения в метрах по вертикали и горизонтали.
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    # Вычисляем расстояние между точками.
    distance = math.sqrt(dx * dx + dy * dy)

    return distance


def get_org(add_params=None):
    serv = "https://search-maps.yandex.ru/v1/"
    key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

    map_params = {
        "apikey": key,
        "text": "школа",
        "lang": "ru_RU",
        "ll": ",".join(["49.129465", "55.782"]),
        "spn": ",".join(["0.005", "0.005"]),
        "type": "biz"
    }

    if add_params:
        map_params.update(add_params)

    response = requests.get(serv, params=map_params)
    if not response:
        return None

    # Преобразуем ответ в json-объект
    json_response = response.json()

    # Получаем первую найденную организацию.
    orgs = json_response["features"]
    return orgs[0]
