from typing import Optional

from sqlalchemy.orm import Session

from src.db.models.Geo import Geo
from src.schemas.Geo import GeoSchemaFull, GeoSchemaFromCountryJson


class GeoCrud:
    db: Session

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_with_full_info(self, geo: GeoSchemaFull) -> Geo:
        geo_to_db: Geo = Geo(
            ip=geo.ip,
            continent=geo.continent,
            continent_code=geo.continent_code,
            country=geo.country,
            country_iso=geo.country_iso,
            city=geo.city,
            latitude=geo.latitude,
            longitude=geo.longitude,
            time_zone=geo.time_zone,
            postal=geo.postal,
            metro_code=geo.metro_code)
        self.db.add(geo_to_db)
        self.db.commit()
        self.db.refresh(geo_to_db)
        return geo_to_db

    def create_with_country(self, geo: GeoSchemaFromCountryJson) -> Geo:
        geo_to_db: Geo = Geo(
            ip=geo.ip,
            continent=geo.continent,
            continent_code=geo.continent_code,
            country=geo.country,
            country_iso=geo.country_iso)

        self.db.add(geo_to_db)
        self.db.commit()
        self.db.refresh(geo_to_db)
        return geo_to_db

    def read_by_id(self, _id: int) -> Optional[Geo]:
        return self.db.query(Geo).filter(Geo.id == _id).first()
