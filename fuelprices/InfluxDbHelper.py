import logging
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

class InfluxDb:
    def __init__(self, url, token, organization, bucket):
        logging.debug("Configuring InfluxDB database connection for url: " + url + " organization " + organization + " bucket " + bucket)
        self.organization = organization
        self.bucket = bucket
        client = influxdb_client.InfluxDBClient(url=url, token=token, organization=organization)
        self.write_api = client.write_api(write_options=SYNCHRONOUS)

    def write_fuel_prices(self, fuel_prices):
        logging.info("Writing prices into InfluxDB for " + fuel_prices.fuel_station_name)
        for fuel in fuel_prices.prices:
            logging.debug("Writing " + fuel + " price into InfluxDB" + " for " + fuel_prices.fuel_station_name)
            record = influxdb_client.Point(fuel).tag("fuel_station", fuel_prices.fuel_station_name).time(fuel_prices.timestamp).field("price", fuel_prices.prices[fuel])
            self.write_api.write(bucket=self.bucket, org=self.organization, record=record)
