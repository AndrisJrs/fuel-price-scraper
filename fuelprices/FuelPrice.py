from datetime import datetime, timezone, UTC


class FuelPrice:
    def __init__(self, fuel_station_name, fuel_key, price, location):
        self.fuel_station_name = fuel_station_name
        self.fuel_key = fuel_key
        self.price = price
        self.location = location
        self.timestamp = datetime.now(UTC)
