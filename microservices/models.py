from sqlalchemy import Boolean, Column, Integer, String, Date, REAL, Enum, Numeric, DateTime, SmallInteger
from microservices.database import Base


class Districts(Base):
    __tablename__ = "districts"

    id = Column(Integer, primary_key=True, index=True)
    district = Column(String, unique=True, index=True)


class Regions(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    region = Column(String, unique=True, index=True)

    district = Column(Integer)


class Cities(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, unique=True, index=True)

    region = Column(Integer)

    city_type = Column(Enum("село", "смт", "місто", name="city_type", create_type=False))
    center_type = Column(Enum("районний", "обласний", name="center_type", create_type=False))


class CityRegions(Base):
    __tablename__ = "city_regions"

    id = Column(Integer, primary_key=True, index=True)
    city_region = Column(String, unique=True, index=True)

    city = Column(Integer)

    description = Column(String, unique=True, index=True)
    group_on_site = Column(String, unique=True, index=True)

    region = Column(Integer)

    hot_deals_limit = Column(Numeric, unique=False, index=True)
    prefix_to_site = Column(String, unique=False, index=True)
    is_subdistrict = Column(Boolean)
    new_building_region = Column(Enum("Приморский+Центр", "Киевский+Малиновский", "Суворовский",
                                      name="new_building_region", create_type=False))


class Streets(Base):
    __tablename__ = "streets"

    id = Column(Integer, primary_key=True, index=True)
    street = Column(String, unique=True, index=True)

    city_region = Column(Integer)

    city = Column(Integer)


class Handbooks(Base):
    __tablename__ = "handbooks"

    id = Column(Integer, primary_key=True, index=True)
    handbook = Column(String, unique=True)
    handbook_type = Column(Enum("withdrawal_reason", "condition",
                                "material", "agency",
                                "stair", "heating",
                                "layout", "house_type",
                                name="handbook_types", create_type=False))


class NewBuildings(Base):
    __tablename__ = "new_buildings"

    id = Column(Integer, primary_key=True, index=True)
    new_building = Column(String, unique=True, index=True)
    building = Column(Boolean)

    street = Column(Integer)

    house = Column(String, unique=True, index=True)

    region = Column(Integer)


class Clients(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)