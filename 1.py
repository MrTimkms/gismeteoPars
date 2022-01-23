import requests
from bs4 import BeautifulSoup
from time import sleep
import json
import csv
""" listnameCity=['Джигда', 'Нелькан', 'Аим ', 'Тулучи ', 'Тумнин ', 'Шахтинское ',
             'Шумный', 'Медвежи ', 'Нижнетамбовское', 'Нижние Халбы', 'Новоильиновка', 'Шахтинское ',
             'Долми', 'Катэн', 'Среднехорский', 'Верхний Нерген']
ListnumCity=['233739', '233740', '233738 ', '233756', '233757', '233780',
            '233802', '233797', '233861 ', '1233862  ', '233863', '233875',
            '233810', '233818', '233836  ', '233877']
yearlist=['2016', '2017','2018','2019','2020','2021'] """
listnameCity = ['Джигда']
ListnumCity = ['233739']
yearlist = ['2016']
dictcyty = dict()
for numnameCity in range(0, len(ListnumCity)):
    dictcyty[ListnumCity[numnameCity]] = listnameCity[numnameCity]
urll = "https://www.gismeteo.ru/diary/"
legListnumCity = len(ListnumCity)
urllist = []
for numcity in range(0, legListnumCity):
    urllcity = urll+ListnumCity[numcity]+'/'
    for numyear in range(0, len(yearlist)):
        urlcityyear = urllcity+yearlist[numyear]+'/'
        for nummouth in range(1, 13):
            urlcityyearmouth = urlcityyear+str(nummouth)
            urllist.append(urlcityyearmouth)

#url= "https://www.gismeteo.ru/diary/4853/2021/12/"
legurlall = len(urlcityyearmouth)
print('Всего операций: ' + str(legurlall))
operat = 0
for url in urllist:  # заменить на
    operat=operat+1
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/35.0.1916.47 Safari/537.36',
               'Cookie': "SCookieID=Cookies"}
    data = []

    # получаем месяцГод
    urldata = url.split('/')
    numurldata = len(urldata)
    monthyear = urldata[numurldata-1]+"."+urldata[numurldata-2]
    print('Текщая операция № '+str(operat)+'. ' +
          dictcyty[urldata[4]]+' За '+monthyear+' . осталось операций: '+str(legurlall-operat))
    # Приводим внутрянку  к норм виду
    r = requests.get(url, headers=headers)
    # собираем заголовки таблицы
    table_head_Day = "Дата"
    table_head_tempday = "Температура день"
    table_head_barday = "давление день"
    table_head_cloudinessDAY = "облачность день"
    table_head_phenomenamaEl = "явления день"
    table_head_Wind = "ветер день"
    table_head_tempnight = "Температура вечер"
    table_head_barnight = "давление вечер"
    table_head_cloudinessnight = "облачность вечер"
    table_head_phenomenamaElnight = "явления вечер"
    table_head_Windnight = "ветер вечер"

    with open(f"data/{dictcyty[urldata[4]]}_{monthyear}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                table_head_Day,
                table_head_tempday,
                table_head_barday,
                table_head_cloudinessDAY,
                table_head_phenomenamaEl,
                table_head_Wind,
                table_head_tempnight,
                table_head_barnight,
                table_head_cloudinessnight,
                table_head_phenomenamaElnight,
                table_head_Windnight
            )
        )
    # Задержка 2 секунды
    sleep(2)
    soup = BeautifulSoup(r.text, 'lxml')
    days = soup.findAll('tr')
    # смотрим дни в месяце
    for day in days:
        try:
            # разбор строки
            td = day.findAll('td')
            day = td[0].text+'.'+monthyear
            tempday = td[1].text
            barday = td[2].text
            # Разбор облачности
            cloudinessmas = td[3].findAll('img')[0].get('src').split('/')
            dlcloudiness = len(cloudinessmas)
            cloudiness = cloudinessmas[dlcloudiness-1]
            if cloudiness == 'dull.png':
                cloudinessDAY = "пасмурно"
            elif cloudiness == 'suncl.png':
                cloudinessDAY = "облачно"
            elif cloudiness == 'sunc.png':
                cloudinessDAY = "малооблачно"
            elif cloudiness == 'sun.png':
                cloudinessDAY = "ясно"
            else:
                cloudinessDAY = "-"
            # разбор явления
            if td[4].find('img') is not None:
                phenomenamass = td[4].findAll('img')[0].get('src').split('/')
                dlphenomena = len(phenomenamass)
                phenomenama = phenomenamass[dlphenomena-1]
                if phenomenama == 'snow.png':
                    phenomenamaEl = 'снег'
                elif phenomenama == 'storm.png':
                    phenomenamaEl = 'гроза'
                elif phenomenama == 'rain-bw.png':
                    phenomenamaEl = 'дождь'
                else:
                    phenomenamaEl = "-"

            else:
                phenomenamaEl = '-'
            Wind = td[5].text
            tempnight = td[6].text
            barnight = td[7].text
            # Разбор облачности
            if td[8].find('img') is not None:
                cloudinessmas = td[8].findAll('img')[0].get('src').split('/')
                dlcloudiness = len(cloudinessmas)
                cloudiness = cloudinessmas[dlcloudiness-1]
                if cloudiness == 'dull.png':
                    cloudinessnight = "пасмурно"
                elif cloudiness == 'suncl.png':
                    cloudinessnight = "облачно"
                elif cloudiness == 'sunc.png':
                    cloudinessnight = "малооблачно"
                elif cloudiness == 'sun.png':
                    cloudinessnight = "ясно"
                else:
                    cloudinessnight = "-"
            else:
                cloudinessnight = '-'
            # разбор явления
            if td[9].find('img') is not None:
                phenomenamass = td[9].findAll('img')[0].get('src').split('/')
                dlphenomena = len(phenomenamass)
                phenomenama = phenomenamass[dlphenomena-1]
                if phenomenama == 'snow.png':
                    phenomenamaElnight = 'снег'
                elif phenomenama == 'storm.png':
                    phenomenamaElnight = 'гроза'
                elif phenomenama == 'rain-bw.png':
                    phenomenamaElnight = 'дождь'
                else:
                    phenomenamaElnight = "-"

            else:
                phenomenamaElnight = '-'
            Windnight = td[10].text

            data.append(
                {
                    "day": day,
                    "tempday": tempday,
                    "barday": barday,
                    "cloudinessDAY": cloudinessDAY,
                    "phenomenamaEl": phenomenamaEl,
                    "Wind": Wind,
                    "tempnight": tempnight,
                    "barnight": barnight,
                    "cloudinessnight": cloudinessnight,
                    "phenomenamaElnight": phenomenamaElnight,
                    "Windnight": Windnight
                }
            )
            with open(f"data/{dictcyty[urldata[4]]}_{monthyear}.csv", "a", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        day,
                        tempday,
                        barday,
                        cloudinessDAY,
                        phenomenamaEl,
                        Wind,
                        tempnight,
                        barnight,
                        cloudinessnight,
                        phenomenamaElnight,
                        Windnight
                    )
                )

        except:
            print('')
    with open(f"data/{dictcyty[urldata[4]]}_{monthyear}.json", "a", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
