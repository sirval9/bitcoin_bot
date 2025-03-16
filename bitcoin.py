import ssl
import json
import websocket
import requests
from requests.auth import AuthBase
import time
import hmac
import hashlib
import credenciais

class BitstampAuth(AuthBase):
    def __init__(self, api_key, api_secret, username):
        self.api_key = api_key
        self.api_secret = api_secret
        self.username = username

    def __call__(self, request):
        nonce = str(int(time.time() * 1000))
        message = nonce + self.username + self.api_key
        signature = hmac.new(self.api_secret.encode(), msg=message.encode(), digestmod=hashlib.sha256).hexdigest().upper()
        request.headers.update({
            'X-Auth': self.api_key,
            'X-Auth-Signature': signature,
            'X-Auth-Nonce': nonce,
            'X-Auth-Timestamp': nonce,
            'X-Auth-Version': 'v2'
        })
        return request

def cliente():
    return BitstampAuth(credenciais.API_KEY, credenciais.API_SECRET, credenciais.USERNAME)

def comprar(quantidade):
    auth = cliente()
    response = requests.post('https://www.bitstamp.net/api/v2/buy/market/btcusd/', auth=auth, data={'amount': quantidade})
    if response.status_code == 200:
        print("COMPROU")
    else:
        print("Erro ao comprar:", response.text)

def vender(quantidade):
    auth = cliente()
    response = requests.post('https://www.bitstamp.net/api/v2/sell/market/btcusd/', auth=auth, data={'amount': quantidade})
    if response.status_code == 200:
        print("VENDEU")
    else:
        print("Erro ao vender:", response.text)

def ao_abrir(ws):
    print("abriu")
    json_subscribe = """
    {
        "event": "bts:subscribe",
        "data": {
            "channel": "live_trades_btcusd"
        }
    }
    """
    ws.send(json_subscribe)

def ao_fechar(ws):
    print("fechou a conexao")

def ao_erro(ws, erro):
    print("conexao deu erro")
    print(erro)

def ao_receber_mensagem(ws, mensagem):
    mensagem = json.loads(mensagem)
    price = mensagem['data']['price']
    print(price)

    if price > 10000:
        print("Nossa, está muito baixo, vamos comprar")
        comprar(1)  # Adicione a quantidade desejada
    elif price < 9000:
        print("Nossa, está muito alto, vamos vender")
        vender(1)  # Adicione a quantidade desejada
    else:
        print("Ainda está na média, vamos esperar")

if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://ws.bitstamp.net",
                                on_open=ao_abrir,
                                on_close=ao_fechar,
                                on_message=ao_receber_mensagem,
                                on_error=ao_erro)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})