from enum import Enum


class FuelType(Enum):
    PETROL_95 = "fuel_95_price"
    PETROL_98 = "fuel_98_price"
    DIESEL = "fuel_diesel_price"
    PRO_DIESEL = "fuel_pro_diesel_price"
    RENEWABLE_DIESEL = "fuel_renewable_diesel_price"
    LPG = "fuel_lpg_price"
