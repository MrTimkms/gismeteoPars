import requests
import json
import csv
#import pymysql as pymysql
from bs4 import BeautifulSoup
from time import sleep
#from config import host, user, password, db_name
from listYearscitys import yearlist, dictcyty
import datetime

# Подключимся к БД
# try:
#     connection = pymysql.connect(
#         host=host,
#         port=3306,
#         user=user,
#         password=password,
#         database=db_name,
#         charset="utf8",
#         cursorclass=pymysql.cursors.DictCursor
#     )
#     print("Connect")
# except Exception as ex:
#     print("ОШИБКА")
#     print(ex)
# добавим список населенных пунктов и их ИД а также список годов
dicctcytyKeys=dictcyty.keys()
listnameCity=[]
ListnumCity=[]
for dicct in dicctcytyKeys:
    listnameCity.append(dictcyty.get(dicct))
    ListnumCity.append(dicct)
# сформируем список url
urll = "https://www.gismeteo.ru/diary/"
legListnumCity = len(ListnumCity)
urllist = []
#Формируется список url для разбора страниц, какие именно странницы программе разбирать на данные.
#Проходя циклом все элементы массива с id города, добавляя к нему разделитель «/» и проходя цикл годов к этим годам также добавляя «/»
for numcity in range(0, legListnumCity):
    urllcity = urll + ListnumCity[numcity] + '/'
    for numyear in range(0, len(yearlist)):
        urlcityyear = urllcity + yearlist[numyear] + '/'
        for nummouth in range(1, 13):
            urlcityyearmouth = urlcityyear + str(nummouth)
            urllist.append(urlcityyearmouth)
# собираем заголовки таблицы для формирования csv
    table_head_idcity = "id города"
    table_head_Day = "дата"
    table_head_tempday = "Температура день"
    table_head_barday = "давление день"
    table_head_cloudinessDAY = "облачность день"
    table_head_phenomenamaEl = "явления день"
    table_head_wind = "ветер день"
    table_head_tempnight = "температура вечер"
    table_head_barnight = "давление вечер"
    table_head_cloudinessnight = "облачность вечер"
    table_head_phenomenamaElnight = "явления вечер"
    table_head_windnight = "ветер вечер"
# получаем кол-во операций : ' + str(legurlall)' для вывода сообщений
legurlall = len(urllist)
print('Всего операций: ' + str(legurlall))
print('время ожидания: ' + str(int(legurlall)*2.1/60) + " минут")
operat = 0
#формируем общий csv
with open(f"data/{'Всенаселенныезавсевремя'}.csv", "w", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(
        (
            table_head_idcity,
            table_head_Day,
            table_head_tempday,
            table_head_barday,
            table_head_cloudinessDAY,
            table_head_phenomenamaEl,
            table_head_wind,
            table_head_tempnight,
            table_head_barnight,
            table_head_cloudinessnight,
            table_head_phenomenamaElnight,
            table_head_windnight
        )
    )
for url in urllist:
    operat = operat + 1
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/35.0.1916.47 Safari/537.36',
               'Cookie': "SCookieID=Cookies"}
    data = []

    # получаем месяц и Год
    urldata = url.split('/')
    numurldata = len(urldata)
    if len(urldata[numurldata - 1]) == 1:
        monthyear = urldata[numurldata - 2] + "-" + "0" + urldata[numurldata - 1]
    else:
        monthyear = urldata[numurldata - 2] + "-" + urldata[numurldata - 1]
    print('Текщая операция № ' + str(operat) + '. ' +
          dictcyty[urldata[4]] + ' За ' + monthyear + ' . осталось операций: ' + str(legurlall - operat))
   #Получение странницы
    r = requests.get(url, headers=headers)
    # Задержка 2 секунды что бы избежать блокировки со тороны сервиса
    #создание файла выгрузки csv
    with open(f"data/{dictcyty[urldata[4]]}_{monthyear}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                table_head_idcity,
                table_head_Day,
                table_head_tempday,
                table_head_barday,
                table_head_cloudinessDAY,
                table_head_phenomenamaEl,
                table_head_wind,
                table_head_tempnight,
                table_head_barnight,
                table_head_cloudinessnight,
                table_head_phenomenamaElnight,
                table_head_windnight
            )
        )
    sleep(2)
    # приводим внутрянку  к форматированному виду html страницу
    soup = BeautifulSoup(r.text, 'lxml')
    days = soup.findAll('tr')
    # смотрим дни в месяце
    for day in days:
        try:
            # разбор строки
            td = day.findAll('td')
            if bool(td):
                if len(td[0].text) == 1:
                    day = monthyear + "-" + '0' + td[0].text
                else:
                    day = monthyear + "-" + td[0].text
                tempday = td[1].text
                barday = td[2].text
                # Разбор облачности
                cloudinessmas = td[3].findAll('img')[0].get('src').split('/')
                dlcloudiness = len(cloudinessmas)
                cloudiness = cloudinessmas[dlcloudiness - 1]
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
                # По аналогии разбираем и явление, за исключением что может быть пустое значение, проработаем это исключение простым условием,
                # где пустые данные будет в виде «-»
                if td[4].find('img') is not None:
                    phenomenamass = td[4].findAll('img')[0].get('src').split('/')
                    dlphenomena = len(phenomenamass)
                    phenomenama = phenomenamass[dlphenomena - 1]
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
                wind = td[5].text
                if td[6].text == '':
                    tempnight = "-"
                else:
                    tempnight = td[6].text
                if td[7].text == '':
                    barnight = "-"
                else:
                    barnight = td[7].text
                # Разбор облачности
                if td[8].find('img') is not None:
                    cloudinessmas = td[8].findAll('img')[0].get('src').split('/')
                    dlcloudiness = len(cloudinessmas)
                    cloudiness = cloudinessmas[dlcloudiness - 1]
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
                    phenomenama = phenomenamass[dlphenomena - 1]
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
                windnight = td[10].text
                if td[10].text == '':
                    windnight = "-"
                else:
                    windnight = td[10].text
                # Добавление текущих данных
                idcity = urldata[4]
                data.append(
                    {
                        "idcity": idcity,
                        "day": day,
                        "tempday": tempday,
                        "barday": barday,
                        "cloudinessDAY": cloudinessDAY,
                        "phenomenamaEl": phenomenamaEl,
                        "wind": wind,
                        "tempnight": tempnight,
                        "barnight": barnight,
                        "cloudinessnight": cloudinessnight,
                        "phenomenamaElnight": phenomenamaElnight,
                        "windnight": windnight
                    }
                )
                # запись индивидуального csv
                with open(f"data/{dictcyty[idcity]}_{monthyear}.csv", "a", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        (
                            idcity,
                            day,
                            tempday,
                            barday,
                            cloudinessDAY,
                            phenomenamaEl,
                            wind,
                            tempnight,
                            barnight,
                            cloudinessnight,
                            phenomenamaElnight,
                            windnight
                        )
                    )
                    # запись csv общего файла
                    with open(f"data/{'Всенаселенныезавсевремя'}.csv", "a", encoding="utf-8") as file:
                        writer = csv.writer(file)
                        writer.writerow(
                            (
                                idcity,
                                day,
                                tempday,
                                barday,
                                cloudinessDAY,
                                phenomenamaEl,
                                wind,
                                tempnight,
                                barnight,
                                cloudinessnight,
                                phenomenamaElnight,
                                windnight
                            )
                        )

                # попытка Запись в БД.
                # На данный момент не получилось добиться записи в бд
                iddiary = int(
                    str(idcity) + str(urldata[numurldata - 2]) + str(urldata[numurldata - 1]))
            #     try:
            #         with connection.cursor() as cursor:
            #             sql = """ INSERT INTO diary (day, tempday, barday, cloudinessDAY, phenomenamaEl, wind, tempnight,
            #             barnight, cloudinessnight, phenomenamaElnight, windnight, city_idcity)
            #             VALUES=(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            #             record = (
            #             datetime.date.fromisoformat(day), tempday, barday, cloudinessDAY, phenomenamaEl, wind, tempnight,
            #             barnight, cloudinessnight, phenomenamaElnight, windnight, int(idcity))
            #             cursor.execute(sql, record)
            #             connection.commit()
            #             print('Комит успешен')
            #     finally:
            #         connection.close()
            # except Exception as exx:
            #     print(exx)
        except Exception as ex:
            print(ex)
    # запись json индивидуального файла
    with open(f"data/{dictcyty[idcity]}_{monthyear}.json", "a", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    # запись json общего файла
    with open(f"data/{'Всенаселенныезавсевремя'}_.json", "a", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)