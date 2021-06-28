from sqlalchemy import Column, Float, Integer, String

from src.db.database import Base


class Geo(Base):
    __tablename__ = "geo"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, unique=True)
    continent = Column(String)
    continent_code = Column(String)
    country = Column(String)
    country_iso = Column(String)
    city = Column(String, nullable=True)
    latitude = Column(Float)
    longitude = Column(Float)
    time_zone = Column(String)
    postal = Column(String, nullable=True)
    metro_code = Column(Integer, nullable=True)
