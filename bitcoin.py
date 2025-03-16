import ssl
import json

import websocket

def comprar():
    print("comprou")
    
def vender():
    print("VENDEU")
    
def ao_abrir(ws):
    print("abriu")
    
    json_subcribe = """
{
    "event": "bts:subscribe",
    "data": {
        "channel": "live_trades_btcusd"
    }
}
"""
               
    ws.send(json_subcribe)
def ao_fechar(ws):
    print("fechou a conexao")
               
def ao_erro(ws,erro):
    print("conexao deu erro")
    print(erro)
             
def ao_receber_mensagem(ws, mensagem):
    mensagem = json.loads(mensagem)
    price = mensagem['data']['price']
    print(price)
            
               
    if price < 10:
        print("Nossa, está muito baixo, vamos comprar")
        comprar()
if __name__ == "__main__":
    

    ws = websocket.WebSocketApp("wss://ws.bitstamp.net.",
                                on_open=ao_abrir,
                                on_close=ao_fechar,
                                on_message=ao_receber_mensagem,
                                on_error=ao_erro)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})                  
                        
    
    
   