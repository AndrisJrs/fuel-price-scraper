from fuelprices.FuelPrices import FuelPrices

class GasStations:
    def get_circlek_prices():
        station_name = "CircleK"
        url = "https://www.circlek.lv/priv%C4%81tperson%C4%81m/degvielas-cenas"
        fuel_95_css_selector = '.ck-striped-table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)'
        fuel_98_css_selector = '.ck-striped-table > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)'
        fuel_diesel_css_selector = '.ck-striped-table > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(2)'
        fuel_lpg_css_selector = '.ck-striped-table > tbody:nth-child(2) > tr:nth-child(4) > td:nth-child(2)'
        
        return FuelPrices.get_fuel_prices(station_name, url, fuel_95_css_selector, fuel_98_css_selector, fuel_diesel_css_selector, fuel_lpg_css_selector)

    def get_neste_prices():
        station_name = "Neste"
        url = "https://www.neste.lv/lv/content/degvielas-cenas"
        fuel_95_css_selector = '.field__item > table:nth-child(3) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > p:nth-child(1) > span:nth-child(1) > strong:nth-child(1)'
        fuel_98_css_selector = '.field__item > table:nth-child(3) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2) > p:nth-child(1) > span:nth-child(1) > strong:nth-child(1)'
        fuel_diesel_css_selector = '.field__item > table:nth-child(3) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(2) > p:nth-child(1) > span:nth-child(1) > strong:nth-child(1)'
        fuel_lpg_css_selector = None
        
        return FuelPrices.get_fuel_prices(station_name, url, fuel_95_css_selector, fuel_98_css_selector, fuel_diesel_css_selector, fuel_lpg_css_selector)

    def get_virsi_prices():
        station_name = "Virši"
        url = "https://www.virsi.lv/lv/privatpersonam/degviela/degvielas-un-elektrouzlades-cenas"
        fuel_95_css_selector = 'div.prices-block:nth-child(2) > div:nth-child(1) > ul:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > p:nth-child(2) > span:nth-child(2)'
        fuel_98_css_selector = 'div.prices-block:nth-child(2) > div:nth-child(1) > ul:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > p:nth-child(2) > span:nth-child(2)'
        fuel_diesel_css_selector = 'div.prices-block:nth-child(2) > div:nth-child(1) > ul:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > p:nth-child(2) > span:nth-child(2)'
        fuel_lpg_css_selector = 'div.price-card:nth-child(5) > div:nth-child(1) > div:nth-child(1) > p:nth-child(2) > span:nth-child(2)'
        
        return FuelPrices.get_fuel_prices(station_name, url, fuel_95_css_selector, fuel_98_css_selector, fuel_diesel_css_selector, fuel_lpg_css_selector)