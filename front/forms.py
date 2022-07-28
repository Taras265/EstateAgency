from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, FloatField, BooleanField, \
    TextAreaField, HiddenField, EmailField, PasswordField, DateField
from wtforms.validators import DataRequired, Optional


class DistrictForm(FlaskForm):
    district = StringField("Название области: ", validators=[DataRequired()])


class RegionForm(FlaskForm):
    region = StringField("Название района: ", validators=[DataRequired()])
    district = SelectField("Область: ", choices=[])


class CityForm(FlaskForm):
    city = StringField("Название города: ", validators=[DataRequired()])
    region = SelectField("Район: ", choices=[])
    city_type = SelectField("Тип города: ", choices=[("село", "село"), ("смт", "смт"), ("місто", "місто")])
    center_type = SelectField("Тип центра: ",
                              choices=[("районний", "районний"), ("обласний", "обласний"), (None, None)],
                              validators=[Optional()])


class CityRegionForm(FlaskForm):
    city_region = StringField("Название района города: ", validators=[DataRequired()])
    city = SelectField("Город: ", choices=[])
    description = StringField("Описание: ", validators=[Optional()])
    group_on_site = StringField("Группа на сайт: ", validators=[Optional()])
    region = SelectField("Район: ", choices=[], validators=[Optional()])
    hot_deals_limit = FloatField("Предел горячих предложений: ", validators=[DataRequired()])
    prefix_to_site = StringField("Префикс на сайт: ", validators=[Optional()])
    is_subdistrict = BooleanField("Подрайон?", validators=[Optional()])
    new_building_region = SelectField("Район новостроя: ",
                                      choices=[("Приморский+Центр", "Приморский+Центр"),
                                               ("Киевский+Малиновский", "Киевский+Малиновский"),
                                               ("Суворовский", "Суворовский"),
                                               (None, None)], validators=[Optional()])


class StreetForm(FlaskForm):
    street = StringField("Название улицы: ", validators=[DataRequired()])
    city_region = SelectField("Район города: ", choices=[])
    city = SelectField("Город: ", choices=[])


class HandbookForm(FlaskForm):
    handbook = StringField("Причина снятия:", validators=[DataRequired()])
    handbook_type = SelectField("Тип справочника: ", choices=[("withdrawal_reason", "Причина снятия"),
                                                              ("condition", "Состояние"),
                                                              ("material", "Материал"),
                                                              ("agency", "Агенство"),
                                                              ("stair", "Лесница"),
                                                              ("heating", "Отопление"),
                                                              ("layout", "Планировка"),
                                                              ("house_type", "Тип дома")],
                                validators=[DataRequired()])


class ClientForm(FlaskForm):
    email = EmailField("Почта: ", validators=[DataRequired()])
    first_name = StringField("Имя: ", validators=[DataRequired()])
    last_name = StringField("Фамилия: ", validators=[DataRequired()])
    phone = StringField("Номер телефона: ", validators=[DataRequired()])


class SeparationForm(FlaskForm):
    separation = StringField("Название филиала: ", validators=[DataRequired()])


class NewBuildingForm(FlaskForm):
    new_building = StringField("Название новостроя: ", validators=[DataRequired()])
    building = BooleanField("Стройка: ", validators=[Optional()])
    street = SelectField("Улица: ", choices=[])
    house = StringField("Дом: ", validators=[DataRequired()])
    region = SelectField("Район города: ", choices=[])


class ObjectsForm(FlaskForm):
    date_before_temporarily_removed = DateField("Дата перед временным удалением (не обязательно): ",
                                                validators=[Optional()])
    deposit_date = DateField("Дата задатка (не обязательно): ", validators=[Optional()])
    purchase_date = DateField("Дата покупки: ", validators=[DataRequired()])
    sale_date = DateField("Дата продажи (не обязательно): ", validators=[Optional()])
    date_of_next_call = DateField("Дата следующего прозвона (не обязательно): ", validators=[Optional()])
    exclusive = BooleanField("Эксклюзив?", validators=[Optional()])
    exclusive_to = DateField("Эксклюзив до (не обязательно): ", validators=[Optional()])
    exclusive_from = DateField("Эксклюзив от (не обязательно): ", validators=[Optional()])
    district = SelectField("Область: ", choices=[], validators=[DataRequired()])
    region = SelectField("Район: ", choices=[], validators=[DataRequired()])
    city = SelectField("Город: ", choices=[], validators=[DataRequired()])
    city_region = SelectField("Район города: ", choices=[], validators=[DataRequired()])
    street = SelectField("Улица: ", choices=[], validators=[DataRequired()])
    house = StringField("Дом (не обязательно): ", validators=[Optional()])
    apartment = StringField("Квартира (не обязательно): ", validators=[Optional()])
    on_site = BooleanField("На сайт?", validators=[Optional()])
    inspection_flag = BooleanField("Осмотрено?", validators=[Optional()])
    paid_exclusive_flag = BooleanField("Платный эксклюзив?", validators=[Optional()])
    terrace_flag = BooleanField("Тераса?", validators=[Optional()])
    sea_flag = BooleanField("У моря?", validators=[Optional()])
    vip = BooleanField("Вип?", validators=[Optional()])
    withdrawal_reason = SelectField("Причина снятия (необязательно): ", choices=[], validators=[Optional()])
    independent = BooleanField("Самостоятельный?", validators=[Optional()])
    condition = SelectField("Состояние: ", choices=[], validators=[DataRequired()])
    special = BooleanField("Специальное предложение?", validators=[Optional()])
    urgently = BooleanField("Срочно?", validators=[Optional()])
    trade = BooleanField("Торг?", validators=[Optional()])
    material = SelectField("Материал: ", choices=[], validators=[DataRequired()])
    status = SelectField("Статус: ", choices=[("В продаже", "В продаже"),
                                              ("Задаток", "Задаток"),
                                              ("Снята", "Снята"),
                                              ("Продана", "Продана")], validators=[DataRequired()])
    object_type = SelectField("Тип объекта: ", choices=[], validators=[DataRequired()])
    square = IntegerField("Площадь: ", validators=[DataRequired()])
    price = IntegerField("Цена: ", validators=[DataRequired()])
    site_price = IntegerField("Цена на сайт: ", validators=[DataRequired()])
    square_meter_price = IntegerField("Цена за кв метор: ", validators=[DataRequired()])
    realtor = SelectField("Риелтор: ", choices=[], validators=[DataRequired()])
    site_realtor1 = SelectField("Риелтор на сайт: ", choices=[], validators=[DataRequired()])
    site_realtor2 = SelectField("Риелтор на сайт 2 (не обязательно): ", choices=[], validators=[Optional()])
    realtor_5_5 = SelectField("Риелтор 5 на 5 (не обязательно): ", choices=[], validators=[Optional()])
    for_trainee = BooleanField("Стажер?", validators=[Optional()])
    realtor_notes = TextAreaField("Заметки риелтора (не обязательно): ", validators=[Optional()])
    reference_point = StringField("Ориентир (не обязательно): ", validators=[Optional()])
    owner = SelectField("Владелец: ", choices=[], validators=[DataRequired()])
    client = SelectField("Клиент (не обязательно): ", choices=[], validators=[Optional()])
    owners_number = IntegerField("Число владельцев: ", validators=[DataRequired()])
    comment = TextAreaField("Коментарий (не обязательно): ", validators=[Optional()])
    separation = SelectField("Филиал: ", choices=[], validators=[DataRequired()])
    agency = SelectField("Агенство: ", choices=[], validators=[DataRequired()])
    agency_sales = SelectField("Агенство продажи: ", choices=[], validators=[DataRequired()])
    sale_terms = StringField("Условия продажи (не обязательно): ", validators=[Optional()])
    filename_of_exclusive_agreement = StringField("Имя файла эксклюзивного соглашения (не обязательно): ",
                                                  validators=[Optional()])
    inspection_file_name = StringField("Имя файла инспекции (не обязательно): ", validators=[Optional()])
    document = StringField("Документ (не обязательно): ", validators=[Optional()])
    filename_forbid_sale = StringField("Имя файла запрета продажи (не обязательно): ", validators=[Optional()])
    new_building_name = SelectField("Название новостроя (не обязательно): ", choices=[], validators=[Optional()])
    new_building = BooleanField("Новострой?", validators=[Optional()])
    new_building_type = SelectField("Тип новостроя: ", choices=[("От хозяина", "От хозяина"),
                                                                ("От строителя", "От строителя"),
                                                                (None, None)],
                                    validators=[Optional()])


class ApartmentsForm(FlaskForm):
    rooms_number = IntegerField("Число комнат: ", validators=[DataRequired()])
    room_types = SelectField("Тип комнат: ", choices=[("Смежные", "Смежные"),
                                                      ("Раздельные", "Раздельные"),
                                                      ("Кухня-студия", "Кухня-студия")],
                             validators=[DataRequired()])
    height = FloatField("Высота: ", validators=[DataRequired()])
    kitchen_square = IntegerField("Площадь кухни: ", validators=[DataRequired()])
    living_square = IntegerField("Жилая площадь: ", validators=[DataRequired()])
    gas = BooleanField("Газ?", validators=[Optional()])
    courtyard = BooleanField("Двор?", validators=[Optional()])
    balcony_number = IntegerField("Число балконов: ", validators=[DataRequired()])
    registered_number = IntegerField("Число прописаных: ", validators=[DataRequired()])
    child_registered_number = IntegerField("Число прописанных детей: ", validators=[DataRequired()])
    loggias_number = IntegerField("Количество лоджий: ", validators=[DataRequired()])
    bay_windows_number = IntegerField("Количество эркеров: ", validators=[DataRequired()])
    commune = BooleanField("Коммуна?", validators=[Optional()])
    frame = StringField("Корпус: ", validators=[DataRequired()])
    stair = SelectField("Лестница: ", choices=[], validators=[DataRequired()])
    balcony = BooleanField("Балкон?", validators=[Optional()])
    heating = SelectField("Отопление: ", choices=[], validators=[DataRequired()])
    office = BooleanField("Офис?", validators=[Optional()])
    penthouse = BooleanField("Пентхаус?", validators=[Optional()])
    redevelopment = SelectField("Перепланировка: ", choices=[("Узаконенная", "Узаконенная"),
                                                             ("Неузаконенная", "Неузаконенная")],
                                validators=[DataRequired()])
    layout = SelectField("Планировка: ", choices=[], validators=[DataRequired()])
    construction_number = StringField("Строительный номер: ", validators=[DataRequired()])
    house_type = SelectField("Тип дома: ", choices=[], validators=[DataRequired()])
    two_level_apartment = BooleanField("Двухуровневая квартира?", validators=[Optional()])
    loggia = IntegerField("Лоджия: ", validators=[DataRequired()])
    attic = BooleanField("Мансарда?", validators=[Optional()])
    electric_stove = BooleanField("Электроплита?", validators=[Optional()])
    floor = IntegerField("Этаж: ", validators=[DataRequired()])
    storeys_number = IntegerField("Этажность: ", validators=[DataRequired()])


class UpdateObjectImageForm(FlaskForm):
    id = HiddenField()
    on_site = BooleanField("На сайт?", validators=[DataRequired()])


class Register(FlaskForm):
    email = EmailField("Почта: ", validators=[DataRequired()])
    first_name = StringField("Имя: ", validators=[DataRequired()])
    last_name = StringField("Фамилия: ", validators=[DataRequired()])
    phone = StringField("Номер телефона: ", validators=[DataRequired()])
    password = PasswordField("Пароль: ", validators=[DataRequired()])
    second_password = PasswordField("Пароль еще раз: ", validators=[DataRequired()])


class Authorization(FlaskForm):
    email = EmailField("Почта: ", validators=[DataRequired()])
    password = PasswordField("Пароль: ", validators=[DataRequired()])


class ObjectTypeForm(FlaskForm):
    type = StringField("Тип: ", validators=[DataRequired()])
