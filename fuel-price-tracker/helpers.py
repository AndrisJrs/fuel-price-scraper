import requests

def get_circlek_prices():
    response = requests.get("https://www.circlek.lv/priv%C4%81tperson%C4%81m/degvielas-cenas")
    print(response.text)

get_circlek_prices()