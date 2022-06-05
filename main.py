import requests
import json
from flask import Flask


def get_valutes_list():
    # ф-я возврат дату курса и список словарей

    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = requests.get(url)
    data = json.loads(response.text)
    day = data['Date'].split('T')
    valutes = list(data['Valute'].values())
    return day, valutes

app = Flask(__name__)

def create_html(den, valutes):
    # ф-я создает таблицу в html формате
    # аргументы : день , список словарей валюты

    # заголовок таблицы
    text = '<h1>'+'Курс валют в руб. на '+den[0] + '</h1>'
    text += '<table>'
    text += '<tr>'
    text += '<th>Код</th>'
    text += '<th>Номинал</th>'
    text += '<th>Наименование</th>'
    text += '<th>Курс</th>'
    text += '<th>Изменение</th>'
    text += '</tr>'

    for valute in valutes:
        # проход по словарю вывод в каждой строке одной валюты
        text += '<tr>'
        text += '<td>'+valute['CharCode']+'</td>'
        text += '<td>' + str(valute['Nominal']) + '</td>'
        text += '<td>' + valute['Name'] + '</td>'
        text += '<td>' + str(valute['Value']) + '</td>'
        izm = round( (valute['Value']-valute['Previous'])/valute['Previous']*100,2)
        if izm<0 :
            sizm = ''+str(izm)
        elif izm>0 :
            sizm = '+' + str(izm)
        else:
            sizm = '0'
        sizm += ' %'
        text += '<td>' + sizm + '</td>'
        text += '</tr>'

    text += '</table>'
    return text


@app.route("/")
def index():
    den, valutes = get_valutes_list()
    html = create_html(den , valutes)
    return html


if __name__ == "__main__":
    app.run()