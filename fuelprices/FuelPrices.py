import requests
import re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

class FuelPrices:
  def __init__(self, fuel_station_name, prices):
    self.fuel_station_name = fuel_station_name
    self.prices = prices
    self.timestamp = datetime.now(timezone.utc)

  def get_fuel_prices(station_name, url, fuel_95_css_selector, fuel_98_css_selector, fuel_diesel_css_selector, fuel_lpg_css_selector):
    float_regex = r"\d+(?:\.\d+)?"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    prices = {}

    if fuel_95_css_selector is not None:
      fuel_95_price_object = soup.select(fuel_95_css_selector)[0].text
      prices['fuel_95_price'] = float(re.findall(float_regex, fuel_95_price_object)[0])
     
    if fuel_98_css_selector is not None:
      fuel_98_price_object = soup.select(fuel_98_css_selector)[0].text
      prices['fuel_98_price'] = float(re.findall(float_regex, fuel_98_price_object)[0])

    if fuel_diesel_css_selector is not None:
      fuel_diesel_price_object = soup.select(fuel_diesel_css_selector)[0].text
      prices['fuel_diesel_price'] = float(re.findall(float_regex, fuel_diesel_price_object)[0])

    if fuel_lpg_css_selector is not None:
      fuel_lpg_price_object = soup.select(fuel_lpg_css_selector)[0].text
      prices['fuel_lpg_price'] = float(re.findall(float_regex, fuel_lpg_price_object)[0])

    return FuelPrices(station_name, prices)