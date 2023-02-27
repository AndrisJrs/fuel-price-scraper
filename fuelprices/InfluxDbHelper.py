import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

class InfluxDb:
    def __init__(self, url, token, organization, bucket):
        self.organization = organization
        self.bucket = bucket
        client = influxdb_client.InfluxDBClient(url=url, token=token, organization=organization)
        self.write_api = client.write_api(write_options=SYNCHRONOUS)

    def write_fuel_prices(self, fuel_prices):
        for fuel in fuel_prices.prices:
            record = influxdb_client.Point(fuel).tag("fuel_station", fuel_prices.fuel_station_name).time(fuel_prices.timestamp).field("price", fuel_prices.prices[fuel])
            self.write_api.write(bucket=self.bucket, org=self.organization, record=record)
