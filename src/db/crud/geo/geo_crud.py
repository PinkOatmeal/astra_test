from sqlalchemy.orm import Session
from src.db.models.Geo import Geo
from src.schemas.Geo import GeoSchemaFull


class GeoCrud:
    db: Session

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, geo: GeoSchemaFull) -> Geo:
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

    def read(self, _id: int):
        return self.db.query(Geo).filter(Geo.id == _id).first()
