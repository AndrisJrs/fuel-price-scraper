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
        for fuel_price in fuel_prices:
            logging.info("Writing fuel" + fuel_price.fuel_key + " with price " + str(fuel_price.price) + " into InfluxDB for " + fuel_price.fuel_station_name)
            record = influxdb_client.Point(fuel_price.fuel_key).tag("fuel_station", fuel_price.fuel_station_name).time(fuel_price.timestamp).field("price", fuel_price.price).field("location", fuel_price.location)
            self.write_api.write(bucket=self.bucket, org=self.organization, record=record)
