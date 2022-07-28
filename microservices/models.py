from sqlalchemy import Boolean, Column, Integer, String, Date, REAL, Enum, Numeric, DateTime, SmallInteger
from microservices.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    phone = Column(String)


class Groups(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    group = Column(String, index=True)


class Rights(Base):
    __tablename__ = "rights"

    id = Column(Integer, primary_key=True, index=True)
    right = Column(String, index=True)
    slug = Column(String, index=True)


class UserGroup(Base):
    __tablename__ = "user_group"

    id = Column(Integer, primary_key=True, index=True)

    group = Column(Integer)

    user = Column(Integer)


class GroupRight(Base):
    __tablename__ = "group_right"

    id = Column(Integer, primary_key=True, index=True)

    group = Column(Integer)

    right = Column(Integer)


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


class ObjectTypes(Base):
    __tablename__ = "object_types"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, unique=True, index=True)
    slug = Column(String, unique=True, index=True)


class Separations(Base):
    __tablename__ = "separations"

    id = Column(Integer, primary_key=True, index=True)
    separation = Column(String, unique=True, index=True)


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


class Objects(Base):
    __tablename__ = "objects"

    id = Column(Integer, primary_key=True, index=True)
    create_date = Column(Date)
    date_before_temporarily_removed = Column(Date)
    deposit_date = Column(Date)
    purchase_date = Column(Date)
    sale_date = Column(Date)
    date_of_next_call = Column(Date)
    inspection_form = Column(DateTime)
    exclusive = Column(Boolean)
    exclusive_to = Column(Date)
    exclusive_from = Column(Date)

    district = Column(Integer)

    region = Column(Integer)

    city = Column(Integer)

    city_region = Column(Integer)

    street = Column(Integer)

    house = Column(String)
    apartment = Column(String)
    on_site = Column(Boolean)
    inspection_flag = Column(Boolean)
    paid_exclusive_flag = Column(Boolean)
    terrace_flag = Column(Boolean)
    sea_flag = Column(Boolean)
    vip = Column(Boolean)

    withdrawal_reason = Column(Integer)

    independent = Column(Boolean)

    condition = Column(Integer)

    special = Column(Boolean)
    urgently = Column(Boolean)
    trade = Column(Boolean)

    material = Column(Integer)

    status = Column(Enum("В продаже", "Задаток", "Снята",
                         "Продана", "Снята совсем", name="status",
                         create_type=False))

    object_type = Column(Integer)

    square = Column(Integer)
    price = Column(Integer)
    site_price = Column(Integer)
    square_meter_price = Column(Integer)

    realtor = Column(Integer)

    site_realtor1 = Column(Integer)

    site_realtor2 = Column(Integer)

    realtor_5_5 = Column(Integer)

    for_trainee = Column(Boolean)
    realtor_notes = Column(String)
    reference_point = Column(String)

    author = Column(Integer)

    owner = Column(Integer)

    client = Column(Integer)

    owners_number = Column(SmallInteger)

    comment = Column(String)

    separation = Column(Integer)

    agency = Column(Integer)

    agency_sales = Column(Integer)

    sale_terms = Column(String)
    filename_of_exclusive_agreement = Column(String)
    inspection_file_name = Column(String)
    document = Column(String)
    filename_forbid_sale = Column(String)

    new_building_name = Column(Integer)

    new_building = Column(Boolean)
    new_building_type = Column(Enum("От хозяина", "От строителя",
                                    name="new_building_types", create_type=False))


class ObjImages(Base):
    __tablename__ = "obj_images"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, unique=False)
    on_site = Column(Boolean, unique=False)

    object = Column(Integer)


class Apartments(Base):
    __tablename__ = "apartments"

    id = Column(Integer, primary_key=True, index=True)
    rooms_number = Column(Integer)
    room_types = Column(Enum("Смежные", "Раздельные", "Кухня-студия",
                             "Комната", name="apartment_types", create_type=False))
    height = Column(REAL)
    kitchen_square = Column(Integer)
    living_square = Column(Integer)
    gas = Column(Boolean)
    courtyard = Column(Boolean)
    balcony_number = Column(SmallInteger)
    registered_number = Column(SmallInteger)
    child_registered_number = Column(SmallInteger)
    loggias_number = Column(SmallInteger)
    bay_windows_number = Column(SmallInteger)
    commune = Column(Boolean)
    frame = Column(String)

    stair = Column(Integer)

    balcony = Column(Boolean)

    heating = Column(Integer)

    office = Column(Boolean)
    penthouse = Column(Boolean)
    redevelopment = Column(Enum("Нет", "Узаконенная", "Неузаконенная",
                                name="redevelopment", create_type=False))

    layout = Column(Integer)

    construction_number = Column(String)

    house_type = Column(Integer)

    two_level_apartment = Column(Boolean)
    loggia = Column(Integer)
    attic = Column(Boolean)
    electric_stove = Column(Boolean)
    floor = Column(Integer)
    storeys_number = Column(Integer)

    object = Column(Integer)
