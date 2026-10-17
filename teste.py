import requests


api = requests.get(" https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL")
resposta = api.json()
a = resposta['USDBRL']['create_date']
b = a.split(" ", 1)
print(b[1])