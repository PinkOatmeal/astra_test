from base64 import b64encode

import requests
from sqlalchemy.orm import Session

from src.db.crud.geo.geo_crud import GeoCrud
from src.db.models.Geo import Geo
from src.exceptions.exceptions import InvalidIPProvided, IPNotFound, ReservedIPProvided
from src.schemas.Geo import GeoSchemaFromCountryJson, GeoSchemaFull
from src.utils.utils import validate_ip
from config import GEOLITE_USER_ID, GEOLITE_API_KEY


class GeoliteController:
    __auth_str: str
    __crud: GeoCrud

    def __init__(self, db: Session, user_id: str = GEOLITE_USER_ID, api_key: str = GEOLITE_API_KEY) -> None:
        self.__auth_str = b64encode(bytes(f"{user_id}:{api_key}", "utf-8")).decode("utf-8")
        self.__crud = GeoCrud(db)

    def fetch_country_info(self, ip: str) -> Geo:
        if validate_ip(ip) is not None:
            raise InvalidIPProvided("Invalid IP-address provided")

        response_json: dict[str, any] = self.__request_to_geolite(f"https://geolite.info/geoip/v2.1/country/{ip}")

        geo_to_db: GeoSchemaFromCountryJson = GeoSchemaFromCountryJson(
            ip=ip,
            continent=response_json["continent"]["names"]["en"],
            continent_code=response_json["continent"]["code"],
            country=response_json["country"]["names"]["en"],
            country_iso=response_json["country"]["iso_code"]
        )

        if self.__crud.ip_entry_exists(ip):
            return self.__crud.update_with_country(geo_to_db)

        return self.__crud.create_with_country(geo_to_db)

    def fetch_city_info(self, ip: str) -> Geo:
        if validate_ip(ip) is not None:
            raise InvalidIPProvided("Invalid IP-address provided")

        response_json: dict[str, any] = self.__request_to_geolite(f"https://geolite.info/geoip/v2.1/city/{ip}")

        geo_to_db: GeoSchemaFull = GeoSchemaFull(
            ip=ip,
            continent=response_json["continent"]["names"]["en"],
            continent_code=response_json["continent"]["code"],
            country=response_json["country"]["names"]["en"],
            country_iso=response_json["country"]["iso_code"],
            city=response_json["city"]["names"]["en"] if "city" in response_json.keys() else None,
            latitude=response_json["location"]["latitude"],
            longitude=response_json["location"]["longitude"],
            time_zone=response_json["location"]["time_zone"],
            postal=response_json["postal"]["code"] if "postal" in response_json.keys() else None,
            metro_code=response_json["location"].get("metro_code")
        )

        if self.__crud.ip_entry_exists(ip):
            return self.__crud.update_with_full_info(geo_to_db)

        return self.__crud.create_with_full_info(geo_to_db)

    def update_all(self) -> None:
        ip_list: list[str] = self.__crud.read_all_ips()
        for ip in ip_list:
            self.fetch_city_info(ip)

    def __request_to_geolite(self, url: str) -> dict[str, any]:
        response = requests.get(url, headers={"Authorization": f"Basic {self.__auth_str}"})
        response_json: dict[str, any] = response.json()

        if response_json.get("code") == "IP_ADDRESS_NOT_FOUND":
            raise IPNotFound("The supplied IP address is not in the geolite database.")

        if response_json.get("code") == "IP_ADDRESS_RESERVED":
            raise ReservedIPProvided(response_json["error"])

        return response_json
