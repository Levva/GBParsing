# Не разобралась с VK OAuth -_-
# Точнее, так и не нашла красивого решения, как настроить запрос таки образом, чтобы не нужно было запускать браузер.
# Была мысть использовать для этих целей webdriver Selenuim. Но, наверняка есть более изящный вариант?
# Поэтом простой вариант с Геокодером и Погодой от Яндекса

import requests
import json

# Мои ключи =)
app_id = '60fc915ac6896441179290628973d765'
yandex_geokoder_key = 'a5e59f47-2a32-40fb-b416-bd6e414f1422'
yandex_weather_key = 'b21694f4-a26f-4a33-9556-eb6b17283e93'
headers = {1: {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'},
           2: {'X-Yandex-API-Key': 'b21694f4-a26f-4a33-9556-eb6b17283e93'}}
city = input('Введите название города: ')
# Раскомментировать, если не хочется ничего вводить:
# city = 'Saint Petersburg'

# Получение данных о погоде с помощью API OpenWeatherMap
openweathermap_link = "https://api.openweathermap.org/data/2.5/weather"
openweathermap_params = {'q': city,
                         'appid': app_id}
response1 = requests.get(openweathermap_link, headers=headers[1], params=openweathermap_params)
if response1.ok:
    data_openweathermap = json.loads(response1.text)
    with open('data_openweathermap.json', 'w', encoding='utf-8') as f:
        json.dump(data_openweathermap, f, ensure_ascii=False, indent=4)
    openweathermap_weather = data_openweathermap["main"]["temp"] - 273.15
else:
    print(f'Город с названием "{city}" не найден на OpenWeatherMap.')
    exit()

# Так как API Yandex.погоды работает с координатами,
# нужно получить координаты заданного города
yandex_coord_link = 'http://geocode-maps.yandex.ru/1.x/'
yandex_map_param = {'format': 'json',
                    'apikey': f'{yandex_geokoder_key}',
                    'results': '1',
                    'geocode': city}
response2 = requests.get(yandex_coord_link, params=yandex_map_param)
if response2.ok:
    data_yandex_geokoder =json.loads(response2.text)
    with open('data_yandex_geokoder.json', 'w', encoding='utf-8') as f:
        json.dump(data_yandex_geokoder, f, ensure_ascii=False, indent=4)
    city_coord = data_yandex_geokoder["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split(' ')
else:
    print(f'Город с названием "{city}" не найден на Яндекс.картах. Невозможно получить координаты.')
    exit()

# Получение данных о погоде с помощью API Yandex.погоды
yandex_weather_link = 'https://api.weather.yandex.ru/v1/forecast'
yandex_weather_params = {'lon': city_coord[0],
                         'lat': city_coord[1]}
response3 = requests.get(yandex_weather_link, headers=headers[2], params=yandex_weather_params)
if response3.ok:
    data_yandex_weather =json.loads(response3.text)
    with open('data_yandex_weather.json', 'w', encoding='utf-8') as f:
        json.dump(data_yandex_weather, f, ensure_ascii=False, indent=4)
    yandex_weather = data_yandex_weather["fact"]["temp"]
else:
    yandex_weather = 0
    print(f'Город с названием "{city}" не найден на Яндекс.погоде. Присвоено занчение по умолчанию.')

print(f'В городе {city}:\nпо данным API OpenWeatherMap температура {openweathermap_weather:.2f} градусов\n'
      f'по данным API Yandex.погоды температура {yandex_weather:.2f} градусов')

