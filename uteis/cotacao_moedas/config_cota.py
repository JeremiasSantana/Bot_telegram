import requests
from aiogram import Router, types
from aiogram.filters import Command




router_moeda_dolar = Router(name='cota_moeda_dolar')



@router_moeda_dolar.message(Command('cotamoedas'))
async def valor_cotacao(menssagem: types.Message):

    api = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL")
    if api.status_code > 200:
        await menssagem.reply("Desculpa, houve um erro ao tentar puxar info da api!! Poderia tentar novamente?")
        return
    
    resposta_json =  api.json()

    atual_dolar =  float(resposta_json['USDBRL']['bid'])
    menor_valor_dolar = float(resposta_json['USDBRL']['low'])
    maior_valor_dolar = float(resposta_json['USDBRL']['high'])

    atual_bit =  float(resposta_json['BTCBRL']['bid'])
    menor_valor_bit = float(resposta_json['BTCBRL']['low'])
    maior_valor_bit = float(resposta_json['BTCBRL']['high'])


    atual_eur =  float(resposta_json['EURBRL']['bid'])
    menor_valor_eur = float(resposta_json['EURBRL']['low'])
    maior_valor_eur = float(resposta_json['EURBRL']['high'])

    hora_consulta = resposta_json['USDBRL']['create_date']
    separa = hora_consulta.split(" ", 1)
    data = separa[0]
    hora = separa[1]
    tabela = f"""
<pre>
╔═════════════════════════════════════════════════════════════╗
║                    📊 COTAÇÃO DE MOEDAS                     ║
╠════════╦══════════════╦══════════════╦══════════════════════╣
║ MOEDA  ║     ATUAL    ║     MÁXIMO   ║       MÍNIMO         ║
╠════════╬══════════════╬══════════════╬══════════════════════╣
║ BTC    ║ {atual_bit:>12.2f} ║ {maior_valor_bit:>12.2f} ║ {menor_valor_bit:>18.2f}   ║
║ DÓLAR  ║ {atual_dolar:>12.2f} ║ {maior_valor_dolar:>12.2f} ║ {menor_valor_dolar:>18.2f}   ║
║ EURO   ║ {atual_eur:>12.2f} ║ {maior_valor_eur:>12.2f} ║ {menor_valor_eur:>18.2f}   ║
╠════════╩══════════════╩══════════════╩══════════════════════╣
║ 📅 DATA: {data:<49}  ║
║ 🕒 HORA: {hora:<49}  ║
╚═════════════════════════════════════════════════════════════╝
</pre>
"""

    await menssagem.reply(
            tabela,
            parse_mode='HTML',
    )


