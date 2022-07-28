from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date, REAL, Enum, Numeric, DateTime, SmallInteger
from sqlalchemy.orm import relationship
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

    group = Column(Integer, ForeignKey("groups.id"))
    group_rel = relationship("Groups", foreign_keys=[group])

    user = Column(Integer, ForeignKey("users.id"))
    user_rel = relationship("Users", foreign_keys=[user])


class GroupRight(Base):
    __tablename__ = "group_right"

    id = Column(Integer, primary_key=True, index=True)

    group = Column(Integer, ForeignKey("groups.id"))
    group_rel = relationship("Groups", foreign_keys=[group])

    right = Column(Integer, ForeignKey("rights.id"))
    right_rel = relationship("Rights", foreign_keys=[right])


class Districts(Base):
    __tablename__ = "districts"

    id = Column(Integer, primary_key=True, index=True)
    district = Column(String, unique=True, index=True)


class Regions(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    region = Column(String, unique=True, index=True)

    district = Column(Integer, ForeignKey("districts.id"))
    district_rel = relationship("Districts", foreign_keys=[district])


class Cities(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, unique=True, index=True)

    region = Column(Integer, ForeignKey("regions.id"))
    region_rel = relationship("Regions", foreign_keys=[region])

    city_type = Column(Enum("село", "смт", "місто", name="city_type", create_type=False))
    center_type = Column(Enum("районний", "обласний", name="center_type", create_type=False))


class CityRegions(Base):
    __tablename__ = "city_regions"

    id = Column(Integer, primary_key=True, index=True)
    city_region = Column(String, unique=True, index=True)

    city = Column(Integer, ForeignKey("cities.id"))
    city_rel = relationship("Cities", foreign_keys=[city])

    description = Column(String, unique=True, index=True)
    group_on_site = Column(String, unique=True, index=True)

    region = Column(Integer, ForeignKey("city_regions.id"))
    region_rel = relationship("CityRegions", remote_side=id, backref="sub_city_regions")

    hot_deals_limit = Column(Numeric, unique=False, index=True)
    prefix_to_site = Column(String, unique=False, index=True)
    is_subdistrict = Column(Boolean)
    new_building_region = Column(Enum("Приморский+Центр", "Киевский+Малиновский", "Суворовский",
                                      name="new_building_region", create_type=False))


class Streets(Base):
    __tablename__ = "streets"

    id = Column(Integer, primary_key=True, index=True)
    street = Column(String, unique=True, index=True)

    city_region = Column(Integer, ForeignKey("city_regions.id"))
    city_region_rel = relationship("CityRegions", foreign_keys=[city_region])

    city = Column(Integer, ForeignKey("cities.id"))
    city_rel = relationship("Cities", foreign_keys=[city])


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

    street = Column(Integer, ForeignKey("streets.id"))
    street_rel = relationship("Streets", foreign_keys=[street])

    house = Column(String, unique=True, index=True)

    region = Column(Integer, ForeignKey("city_regions.id"))
    region_rel = relationship("CityRegions", foreign_keys=[region])


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

    district = Column(Integer, ForeignKey("districts.id"))
    district_obj = relationship("Districts", foreign_keys=[district])

    region = Column(Integer, ForeignKey("regions.id"))
    region_obj = relationship("Regions", foreign_keys=[region])

    city = Column(Integer, ForeignKey("cities.id"))
    city_obj = relationship("Cities", foreign_keys=[city])

    city_region = Column(Integer, ForeignKey("city_regions.id"))
    city_region_rel = relationship("CityRegions", foreign_keys=[city_region])

    street = Column(Integer, ForeignKey("streets.id"))
    street_obj = relationship("Streets", foreign_keys=[street])

    house = Column(String)
    apartment = Column(String)
    on_site = Column(Boolean)
    inspection_flag = Column(Boolean)
    paid_exclusive_flag = Column(Boolean)
    terrace_flag = Column(Boolean)
    sea_flag = Column(Boolean)
    vip = Column(Boolean)

    withdrawal_reason = Column(Integer, ForeignKey("handbooks.id"))
    withdrawal_reason_rel = relationship("Handbooks", foreign_keys=[withdrawal_reason])

    independent = Column(Boolean)

    condition = Column(Integer, ForeignKey("handbooks.id"))
    condition_rel = relationship("Handbooks", foreign_keys=[condition])

    special = Column(Boolean)
    urgently = Column(Boolean)
    trade = Column(Boolean)

    material = Column(Integer, ForeignKey("handbooks.id"))
    material_rel = relationship("Handbooks", foreign_keys=[material])

    status = Column(Enum("В продаже", "Задаток", "Снята",
                         "Продана", "Снята совсем", name="status",
                         create_type=False))

    object_type = Column(Integer, ForeignKey("object_types.id"))
    type_obj = relationship("ObjectTypes", foreign_keys=[object_type])

    square = Column(Integer)
    price = Column(Integer)
    site_price = Column(Integer)
    square_meter_price = Column(Integer)

    realtor = Column(Integer, ForeignKey("users.id"))
    realtor_obj = relationship("Users", foreign_keys=[realtor])

    site_realtor1 = Column(Integer, ForeignKey("users.id"))
    realtor1_obj = relationship("Users", foreign_keys=[site_realtor1])

    site_realtor2 = Column(Integer, ForeignKey("users.id"))
    realtor2_obj = relationship("Users", foreign_keys=[site_realtor2])

    realtor_5_5 = Column(Integer, ForeignKey("users.id"))
    realtor_5_5_obj = relationship("Users", foreign_keys=[realtor_5_5])

    for_trainee = Column(Boolean)
    realtor_notes = Column(String)
    reference_point = Column(String)

    author = Column(Integer, ForeignKey("users.id"))
    author_obj = relationship("Users", foreign_keys=[author])

    owner = Column(Integer, ForeignKey("clients.id"))
    owner_obj = relationship("Clients", foreign_keys=[owner])

    client = Column(Integer, ForeignKey("clients.id"))
    client_obj = relationship("Clients", foreign_keys=[client])

    owners_number = Column(SmallInteger)

    comment = Column(String)

    separation = Column(Integer, ForeignKey("separations.id"))
    separation_obj = relationship("Separations", foreign_keys=[separation])

    agency = Column(Integer, ForeignKey("handbooks.id"))
    agency_rel = relationship("Handbooks", foreign_keys=[agency])

    agency_sales = Column(Integer, ForeignKey("handbooks.id"))
    agency_sales_rel = relationship("Handbooks", foreign_keys=[agency_sales])

    sale_terms = Column(String)
    filename_of_exclusive_agreement = Column(String)
    inspection_file_name = Column(String)
    document = Column(String)
    filename_forbid_sale = Column(String)

    new_building_name = Column(Integer, ForeignKey("new_buildings.id"))
    new_building_name_rel = relationship("NewBuildings", foreign_keys=[new_building_name])

    new_building = Column(Boolean)
    new_building_type = Column(Enum("От хозяина", "От строителя",
                                    name="new_building_types", create_type=False))


class ObjImages(Base):
    __tablename__ = "obj_images"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, unique=False)
    on_site = Column(Boolean, unique=False)

    object = Column(Integer, ForeignKey("objects.id"))
    obj = relationship("Objects", foreign_keys=[object])


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

    stair = Column(Integer, ForeignKey("handbooks.id"))
    stair_rel = relationship("Handbooks", foreign_keys=[stair])

    balcony = Column(Boolean)

    heating = Column(Integer, ForeignKey("handbooks.id"))
    heating_rel = relationship("Handbooks", foreign_keys=[heating])

    office = Column(Boolean)
    penthouse = Column(Boolean)
    redevelopment = Column(Enum("Нет", "Узаконенная", "Неузаконенная",
                                name="redevelopment", create_type=False))

    layout = Column(Integer, ForeignKey("handbooks.id"))
    layout_rel = relationship("Handbooks", foreign_keys=[layout])

    construction_number = Column(String)

    house_type = Column(Integer, ForeignKey("handbooks.id"))
    house_type_rel = relationship("Handbooks", foreign_keys=[house_type])

    two_level_apartment = Column(Boolean)
    loggia = Column(Integer)
    attic = Column(Boolean)
    electric_stove = Column(Boolean)
    floor = Column(Integer)
    storeys_number = Column(Integer)

    object = Column(Integer, ForeignKey("objects.id"))
    object_rel = relationship("Objects", foreign_keys=[object])
