import os
import sys

import pygame
import requests

p = [30.3210104, 59.9440931, 30.3188324, 59.9442382,
     30.3173304, 59.9452108, 30.3147984, 59.9459845, 30.3084469, 59.9461995, 30.3023529, 59.9468013,
     30.2972031, 59.9467583, 30.2826118, 59.9495951, 30.2754021, 59.9518301, 30.2681923, 59.9552681,
     30.2621841, 59.9574167, 30.2515411, 59.9587058, 30.2420998, 59.9602526, 30.2342033, 59.9624009,
     30.2266502, 59.9642913, 30.2194405, 59.9657519, 30.2129173, 59.9663534, 30.2038193, 59.9668689,
     30.1936913, 59.9669548, 30.1808167, 59.966697, 30.1648521, 59.9657519, 30.1358414, 59.9608542,
     30.0970459, 59.9514003, 30.0640869, 59.9428035, 30.0270081, 59.9317963, 29.9899292, 59.919581,
     29.9432373, 59.9049511, 29.920578, 59.8956535, 29.9134272, 59.8918648]
points = ','.join([str(x) for x in p])
geocoder_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=Невская губа&format=json"
# Выполняем запрос.
response = requests.get(geocoder_request)
if response:
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    top_cor = ','.join(toponym_coodrinates.split())
else:
    print("Ошибка выполнения запроса:")
    print(geocoder_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
response = None
mp = f"http://static-maps.yandex.ru/1.x/?ll={top_cor}&z=10&l=map&pl=c:{'FF0000'},w:2,{points}&pt={p[0]},{p[1]},pma~{p[-2]},{p[-1]},pmb"
response = requests.get(mp)

if not response:
    print("Ошибка выполнения запроса:")
    print(mp)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

# Запишем полученное изображение в файл.
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)