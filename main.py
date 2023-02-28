import os
from fuelprices.GasStations import GasStations
from fuelprices.InfluxDbHelper import InfluxDb

def main():
    bucket = os.environ['INFLUXDB_BUCKET']
    url = os.environ['INFLUXDB_URL']
    org = os.environ['INFLUXDB_ORG']
    token = os.environ['INFLUXDB_TOKEN']

    circlek_prices = GasStations.get_circlek_prices()
    neste_prices = GasStations.get_neste_prices()
    virsi_prices = GasStations.get_virsi_prices()
    viada_prices = GasStations.get_viada_prices()

    influxdb = InfluxDb(url, token, org, bucket)
    influxdb.write_fuel_prices(circlek_prices)
    influxdb.write_fuel_prices(neste_prices)
    influxdb.write_fuel_prices(virsi_prices)
    influxdb.write_fuel_prices(viada_prices)

if __name__ == '__main__':
    main()