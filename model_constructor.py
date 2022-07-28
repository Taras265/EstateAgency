from sqlalchemy import create_engine, MetaData, Table, Column, \
    Integer, String, Boolean, ForeignKey, Enum, Numeric, Date, REAL, DateTime, SmallInteger

engine = create_engine('postgresql://postgres:1q2w3e4r@localhost/EstateAgency', echo=True)
meta = MetaData()

users = Table(
    'users', meta,
    Column('id', Integer, primary_key=True),
    Column('email', String, unique=True),
    Column('first_name', String),
    Column('last_name', String),
    Column('hashed_password', String),
    Column('is_active', Boolean),
    Column('phone', String, unique=True),
)

groups = Table(
    'groups', meta,
    Column('id', Integer, primary_key=True),
    Column('group', String, unique=True),
)

rights = Table(
    'rights', meta,
    Column('id', Integer, primary_key=True),
    Column('right', String, unique=True),
    Column('slug', String, unique=True),
)

user_group = Table(
    'user_group', meta,
    Column('id', Integer, primary_key=True),
    Column('group', Integer, ForeignKey("groups.id")),
    Column('user', Integer, ForeignKey("users.id")),
)

group_right = Table(
    'group_right', meta,
    Column('id', Integer, primary_key=True),
    Column('group', Integer, ForeignKey("groups.id")),
    Column('right', Integer, ForeignKey("rights.id")),
)

districts = Table(
    'districts', meta,
    Column('id', Integer, primary_key=True),
    Column('district', String, unique=True),
)

regions = Table(
    'regions', meta,
    Column('id', Integer, primary_key=True),
    Column('region', String, unique=True),
    Column('district', Integer, ForeignKey("districts.id")),
)

city_type = Enum("село", "смт", "місто", name="city_type", create_type=False)
center_type = Enum("районний", "обласний", name="center_type", create_type=False)

cities = Table(
    'cities', meta,
    Column('id', Integer, primary_key=True),
    Column('city', String, unique=True),
    Column('region', Integer, ForeignKey("districts.id")),
    Column('city_type', city_type),
    Column('center_type', center_type),
)

new_building_region = Enum("Приморский+Центр", "Киевский+Малиновский", "Суворовский",
                           name="new_building_region", create_type=False)

city_regions = Table(
    'city_regions', meta,
    Column('id', Integer, primary_key=True),
    Column('city_region', String, unique=True),
    Column('city', Integer, ForeignKey("cities.id")),
    Column('description', String),
    Column('group_on_site', String),
    Column('region', Integer, ForeignKey("city_regions.id")),
    Column('hot_deals_limit', Numeric),
    Column('prefix_to_site', String),
    Column('is_subdistrict', Boolean),
    Column('new_building_region', new_building_region),
)

streets = Table(
    'streets', meta,
    Column('id', Integer, primary_key=True),
    Column('street', String, unique=True),
    Column('city_region', Integer, ForeignKey("city_regions.id")),
    Column('city', Integer, ForeignKey("cities.id")),
)

object_types = Table(
    'object_types', meta,
    Column('id', Integer, primary_key=True),
    Column('type', String, unique=True),
    Column('slug', String, unique=True),
)

separations = Table(
    'separations', meta,
    Column('id', Integer, primary_key=True),
    Column('separation', String, unique=True),
)

handbook_types = Enum("withdrawal_reason", "condition",
                      "material", "agency", "stair", "heating",
                      "layout", "house_type",
                      name="handbook_types", create_type=False)

handbooks = Table(
    'handbooks', meta,
    Column('id', Integer, primary_key=True),
    Column('handbook', String, unique=True),
    Column('handbook_type', handbook_types),
)

new_building = Table(
    'new_buildings', meta,
    Column('id', Integer, primary_key=True),
    Column('new_building', String, unique=True),
    Column('building', Boolean),
    Column('street', Integer, ForeignKey("streets.id")),
    Column('house', String),
    Column('region', Integer, ForeignKey("city_regions.id")),
)

clients = Table(
    'clients', meta,
    Column('id', Integer, primary_key=True),
    Column('email', String, unique=True),
    Column('first_name', String),
    Column('last_name', String),
    Column('phone', String, unique=True),
)

new_building_types = Enum("От хозяина", "От строителя", name="new_building_types", create_type=False)
status = Enum("В продаже", "Задаток", "Снята", "Продана", "Снята совсем", name="status", create_type=False)

objects = Table(
    'objects', meta,
    Column('id', Integer, primary_key=True),
    Column('create_date', Date),
    Column('date_before_temporarily_removed', Date),
    Column('deposit_date', Date),
    Column('purchase_date', Date),
    Column('sale_date', Date),
    Column('date_of_next_call', Date),
    Column('inspection_form', DateTime),
    Column('exclusive', Boolean),
    Column('exclusive_to', Date),
    Column('exclusive_from', Date),
    Column('district', Integer, ForeignKey("districts.id")),
    Column('region', Integer, ForeignKey("regions.id")),
    Column('city', Integer, ForeignKey("cities.id")),
    Column('city_region', Integer, ForeignKey("city_regions.id")),
    Column('street', Integer, ForeignKey("streets.id")),
    Column('house', String),
    Column('apartment', String),
    Column('on_site', Boolean),
    Column('inspection_flag', Boolean),
    Column('paid_exclusive_flag', Boolean),
    Column('terrace_flag', Boolean),
    Column('sea_flag', Boolean),
    Column('vip', Boolean),
    Column('withdrawal_reason', Integer, ForeignKey("handbooks.id")),
    Column('independent', Boolean),
    Column('condition', Integer, ForeignKey("handbooks.id")),
    Column('special', Boolean),
    Column('urgently', Boolean),
    Column('trade', Boolean),
    Column('material', Integer, ForeignKey("handbooks.id")),
    Column('status', status),
    Column('object_type', Integer, ForeignKey("object_types.id")),
    Column('square', Integer),
    Column('price', Integer),
    Column('site_price', Integer),
    Column('square_meter_price', Integer),
    Column('realtor', Integer, ForeignKey("users.id")),
    Column('site_realtor1', Integer, ForeignKey("users.id")),
    Column('site_realtor2', Integer, ForeignKey("users.id")),
    Column('realtor_5_5', Integer, ForeignKey("users.id")),
    Column('for_trainee', Boolean),
    Column('realtor_notes', String),
    Column('reference_point', String),
    Column('author', Integer, ForeignKey("users.id")),
    Column('owner', Integer, ForeignKey("clients.id")),
    Column('client', Integer, ForeignKey("clients.id")),
    Column('owners_number', SmallInteger),
    Column('comment', String),
    Column('separation', Integer, ForeignKey("separations.id")),
    Column('agency', Integer, ForeignKey("handbooks.id")),
    Column('agency_sales', Integer, ForeignKey("handbooks.id")),
    Column('sale_terms', String),
    Column('filename_of_exclusive_agreement', String),
    Column('inspection_file_name', String),
    Column('document', String),
    Column('filename_forbid_sale', String),
    Column('new_building_name', Integer, ForeignKey("new_buildings.id")),
    Column('new_building', Boolean),
    Column('new_building_type', new_building_types),
)

obj_images = Table(
    'obj_images', meta,
    Column('id', Integer, primary_key=True),
    Column('source', String, unique=True),
    Column('on_site', Boolean),
    Column('object', Integer, ForeignKey("objects.id")),
)

room_types = Enum("Смежные", "Раздельные", "Кухня-студия", "Комната", name="apartment_types", create_type=False)
redevelopment = Enum("Нет", "Узаконенная", "Неузаконенная", name="redevelopment", create_type=False)

apartments = Table(
    'apartments', meta,
    Column('id', Integer, primary_key=True),
    Column('rooms_number', Integer),
    Column('room_types', room_types),
    Column('height', REAL),
    Column('kitchen_square', Integer),
    Column('living_square', Integer),
    Column('gas', Boolean),
    Column('courtyard', Boolean),
    Column('balcony_number', SmallInteger),
    Column('registered_number', SmallInteger),
    Column('child_registered_number', SmallInteger),
    Column('loggias_number', SmallInteger),
    Column('bay_windows_number', SmallInteger),
    Column('commune', Boolean),
    Column('frame', String),
    Column('stair', Integer, ForeignKey("handbooks.id")),
    Column('balcony', Boolean),
    Column('heating', Integer, ForeignKey("handbooks.id")),
    Column('office', Boolean),
    Column('penthouse', Boolean),
    Column('redevelopment', redevelopment),
    Column('layout', Integer, ForeignKey("handbooks.id")),
    Column('construction_number', String),
    Column('house_type', Integer, ForeignKey("handbooks.id")),
    Column('two_level_apartment', Boolean),
    Column('loggia', Integer),
    Column('attic', Boolean),
    Column('electric_stove', Boolean),
    Column('floor', Integer),
    Column('storeys_number', Integer),
    Column('object', Integer, ForeignKey("objects.id")),
)

meta.create_all(engine)
