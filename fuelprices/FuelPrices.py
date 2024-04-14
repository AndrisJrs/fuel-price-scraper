from datetime import datetime, timezone

class FuelPrice:
  def __init__(self, fuel_station_name, fuel_key, price, location):
    self.fuel_station_name = fuel_station_name
    self.fuel_key = fuel_key
    self.price = price
    self.location = location
    self.timestamp = datetime.now(timezone.utc)
