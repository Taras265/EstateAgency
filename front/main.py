import datetime
import shutil
from datetime import date
from flask import Flask, render_template, request, flash, redirect, session
from api.handbooks.handbooks import *
from api.objects.objects import *
from api.auth.auth import *
from front.forms import *
from front.functions import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "fjkgeruhnslkfnsklklklwfoefnjkls;fkmc\kj;d3iorjO'DAWDFFGfdbHRWgjhf"

district_api = Districts()
region_api = Regions()
city_api = Cities()
city_region_api = CityRegions()
street_api = Streets()
new_building_api = NewBuildings()
catalog_api = ObjectTypes()
object_api = Objects()
apartment_api = Apartments()
object_image_api = ObjectImages()
user_group_api = UserGroups()
right_api = Rights()
group_api = Groups()
separation_api = Separations()
client_api = Clients()


@app.route("/")
def main():
    if not auth_api.check_user_right(session.get("token"), "main"):
        return "403 Error Forbidden"
    types_details = []
    obj_types = catalog_api.get_all()
    for obj_type in obj_types:
        objects = object_api.get_by_category(obj_type.get("id"))
        if objects and isinstance(objects, list):
            images = object_image_api.get_by_object(objects[0].get("id"))
            if images:
                image_name = images[0].get("source")
            else:
                image_name = "default.jpg"
            types_details.append({"type": obj_type.get("type"),
                                  "image_source": f"{OBJECT_IMAGES_URL}/{image_name}",
                                  "objects_count": len(objects),
                                  "id": obj_type.get("id")})
    objects = object_api.get_all()
    objects_detail = get_objects_details(objects)
    rights = check_user_rights(session.get("token"), ["description", "catalog", "handbook", "main",
                                                      "add_handbook", "add_object", "all_types"])
    return render_template('main.html', types_details=types_details, objects=objects_detail[0:3],
                           logged=user_logged(session.get("token")), rights=rights)


@app.route("/catalog/")
def catalog():
    if not auth_api.check_user_right(session.get("token"), "catalog"):
        return "403 Error Forbidden"
    objects = object_api.get_all()
    objects_detail = get_objects_details(objects)
    obj_types = catalog_api.get_all()
    rights = check_user_rights(session.get("token"), ["description", "catalog", "handbook", "main",
                                                      "add_object", "add_handbook", "all_types"])
    return render_template('catalog.html', objects=objects_detail, obj_types=obj_types,
                           logged=user_logged(session.get("token")), rights=rights)


@app.route("/catalog/<int:obj_type>/")
def sorted_catalog(obj_type):
    if not auth_api.check_user_right(session.get("token"), "catalog"):
        return "403 Error Forbidden"
    objects = object_api.get_by_category(obj_type)
    if not isinstance(objects, dict):
        objects_detail = get_objects_details(objects)
    else:
        objects_detail = []
    obj_types = catalog_api.get_all()
    rights = check_user_rights(session.get("token"), ["description", "catalog", "handbook", "main",
                                                      "add_object", "add_handbook", "all_types"])
    return render_template('catalog.html', objects=objects_detail, obj_types=obj_types,
                           logged=user_logged(session.get("token")), rights=rights)


@app.route("/catalog/<int:obj_type>/<int:object_id>/", methods=['POST', 'GET'])
def description(obj_type, object_id):
    if not auth_api.check_user_right(session.get("token"), "description"):
        return "403 Error Forbidden"
    objects = object_api.get_by_category(obj_type)
    obj = object_api.get(object_id)
    if obj not in objects:
        return "404 Error Not Found"
    obj = get_object_detail(obj)
    objects = object_api.get_by_category(obj_type)
    clean_objects = get_objects_details(objects)
    clean_objects.remove(obj)
    obj_types = catalog_api.get_all()
    try:
        import os
        shutil.rmtree("img")
        os.mkdir("img")
    except:
        pass
    rights = check_user_rights(session.get("token"), ["catalog", "handbook", "main", "change_object",
                                                      "delete_object", "add_handbook", "add_object",
                                                      "all_types", "update_details"])
    return render_template('description.html', object=obj, other_objects=clean_objects[0:3],
                           obj_types=obj_types,
                           logged=user_logged(session.get("token")), rights=rights)


@app.route("/handbook/")
@app.route("/handbook/<int:page>/")
def handbook(page=1):
    if not auth_api.check_user_right(session.get("token"), "handbook"):
        return "403 Error Forbidden"
    on_page = 15
    districts = district_api.get_all()

    regions_dict, regions, region_pages = handbook_sort(region_api, [page * on_page - on_page, on_page], on_page)
    if page > region_pages:
        regions = region_api.get_on_page(region_pages * on_page - on_page, on_page).get("objects")
    region = handbook_pages("regions", regions, ["district", ], {"district": district_api}, page, region_pages)

    cities_dict, cities, city_pages = handbook_sort(city_api, [page * on_page - on_page, on_page], on_page)
    if page > city_pages:
        cities = city_api.get_on_page(city_pages * on_page - on_page, on_page).get("objects")
    city = handbook_pages("cities", cities, ["region", ], {"region": region_api}, page, city_pages)

    city_region_dict, city_regions, city_region_pages = handbook_sort(city_region_api,
                                                                      [page * on_page - on_page, on_page],
                                                                      on_page)
    if page > city_region_pages:
        city_regions = city_region_api.get_on_page(city_region_pages * on_page - on_page, on_page).get("objects")
    city_region = handbook_pages("city_regions", city_regions,
                                 ["city", "region"], {"city": city_api, "region": region_api}, page, city_region_pages)

    street_dict, streets, street_pages = handbook_sort(street_api, [page * on_page - on_page, on_page], on_page)
    if page > street_pages:
        streets = street_api.get_on_page(street_pages * on_page - on_page, on_page).get("objects")
    street = handbook_pages("streets", streets,
                            ["city_region", "city"], {"city": city_api, "city_region": city_region_api},
                            page, street_pages)

    client_dict, clients, client_pages = handbook_sort(client_api, [page * on_page - on_page, on_page], on_page)
    if page > client_pages:
        clients = client_api.get_on_page(client_pages * on_page - on_page, on_page).get("objects")
    client = {"clients": clients}
    client.update(standard_pages(page, client_pages))

    separation_dict, separations, separation_pages = handbook_sort(separation_api, [page * on_page - on_page, on_page],
                                                                   on_page)
    if page > separation_pages:
        separations = separation_api.get_on_page(separation_pages * on_page - on_page, on_page).get("objects")
    separation = {"separations": separations}
    separation.update(standard_pages(page, separation_pages))

    withdrawal_reason_dict, withdrawal_reasons, \
    withdrawal_reason_pages = handbook_sort(handbook_api,
                                            ["withdrawal_reason", page * on_page - on_page, on_page],
                                            on_page)
    if page > withdrawal_reason_pages:
        withdrawal_reasons = handbook_api.get_on_page("withdrawal_reason",
                                                      withdrawal_reason_pages * on_page - on_page,
                                                      on_page).get("objects")
    withdrawal_reason = {"withdrawal_reasons": withdrawal_reasons}
    withdrawal_reason.update(standard_pages(page, withdrawal_reason_pages))

    condition_dict, conditions, condition_pages = handbook_sort(handbook_api,
                                                                ["condition", page * on_page - on_page, on_page],
                                                                on_page)
    if page > condition_pages:
        conditions = handbook_api.get_on_page("condition",
                                              condition_pages * on_page - on_page,
                                              on_page).get("objects")
    condition = {"conditions": conditions}
    condition.update(standard_pages(page, condition_pages))

    material_dict, materials, material_pages = handbook_sort(handbook_api,
                                                             ["material", page * on_page - on_page, on_page],
                                                             on_page)
    if page > material_pages:
        materials = handbook_api.get_on_page("material",
                                             material_pages * on_page - on_page,
                                             on_page).get("objects")
    material = {"materials": materials}
    material.update(standard_pages(page, material_pages))

    agency_dict, agencies, agency_pages = handbook_sort(handbook_api,
                                                        ["agency", page * on_page - on_page, on_page],
                                                        on_page)
    if page > agency_pages:
        agencies = handbook_api.get_on_page("agency",
                                            agency_pages * on_page - on_page,
                                            on_page).get("objects")
    agency = {"agencies": agencies}
    agency.update(standard_pages(page, agency_pages))

    new_building_name_dict, new_building_names, new_building_name_pages = handbook_sort(new_building_api,
                                                                                        [page * on_page - on_page,
                                                                                         on_page],
                                                                                        on_page)
    if page > new_building_name_pages:
        new_building_names = new_building_api.get_on_page(new_building_name_pages * on_page - on_page,
                                                          on_page).get("objects")
    new_building_name = {"new_building_names": new_building_names}
    new_building_name.update(standard_pages(page, new_building_name_pages))

    stair_dict, stairs, stair_pages = handbook_sort(handbook_api,
                                                    ["stair",
                                                     page * on_page - on_page,
                                                     on_page],
                                                    on_page)
    if page > stair_pages:
        stairs = handbook_api.get_on_page("stair",
                                          stair_pages * on_page - on_page,
                                          on_page).get("objects")
    stair = {"stairs": stairs}
    stair.update(standard_pages(page, stair_pages))

    heating_dict, heating, heating_pages = handbook_sort(handbook_api,
                                                         ["heating",
                                                          page * on_page - on_page,
                                                          on_page],
                                                         on_page)
    if page > heating_pages:
        heating = handbook_api.get_on_page("heating",
                                           heating_pages * on_page - on_page,
                                           on_page).get("objects")
    heating = {"heating": heating}
    heating.update(standard_pages(page, heating_pages))

    layout_dict, layouts, layout_pages = handbook_sort(handbook_api,
                                                       ["layout",
                                                        page * on_page - on_page,
                                                        on_page],
                                                       on_page)
    if page > layout_pages:
        layouts = handbook_api.get_on_page("layout",
                                           layout_pages * on_page - on_page,
                                           on_page).get("objects")
    layout = {"layouts": layouts}
    layout.update(standard_pages(page, stair_pages))

    house_type_dict, house_types, house_type_pages = handbook_sort(handbook_api,
                                                                   ["house_type",
                                                                    page * on_page - on_page,
                                                                    on_page],
                                                                   on_page)
    if page > house_type_pages:
        house_types = handbook_api.get_on_page("house_type",
                                               house_type_pages * on_page - on_page,
                                               on_page).get("objects")
    house_type = {"house_types": house_types}
    house_type.update(standard_pages(page, house_type_pages))

    rights = check_user_rights(session.get("token"), ["catalog", "handbook", "main",
                                                      "add_handbook", "change_handbook",
                                                      "delete_handbook", "add_object", "all_types"])

    return render_template("handbook.html", districts=districts,
                           region=region, city=city,
                           city_region=city_region, street=street,
                           withdrawal_reason=withdrawal_reason, condition=condition,
                           material=material, separation=separation,
                           agency=agency, client=client,
                           new_building_name=new_building_name,
                           stairs=stair, heating=heating, layouts=layout,
                           house_types=house_type,
                           logged=user_logged(session.get("token")),
                           rights=rights)


@app.route("/handbook/add/", methods=['POST', 'GET'])
def add_handbook():
    if not auth_api.check_user_right(session.get("token"), "add_handbook"):
        return "403 Error Forbidden"
    if district_api.get_all():
        district_choices = [(district.get("id"), district.get("district")) for district in district_api.get_all()]
    else:
        district_choices = [("---", "---")]

    if region_api.get_all():
        region_choices = [(region.get("id"), region.get("region")) for region in region_api.get_all()]
    else:
        region_choices = [("---", "---")]
    if city_api.get_all():
        city_choices = [(city.get("id"), city.get("city")) for city in city_api.get_all()]
    else:
        city_choices = [("---", "---")]

    if city_region_api.get_all():
        city_region_choices = [(city_region.get("id"), city_region.get("city_region")) for city_region in
                               city_region_api.get_all()]
    else:
        city_region_choices = [("---", "---")]

    if street_api.get_all():
        street_choices = [(street.get("id"), street.get("street")) for street in
                          street_api.get_all()]
    else:
        street_choices = [("---", "---")]

    district_form = DistrictForm(request.form)

    region_form = RegionForm(request.form)
    region_form.district.choices = district_choices

    city_form = CityForm(request.form)
    city_form.region.choices = region_choices

    city_region_form = CityRegionForm(request.form)
    city_region_form.city.choices = city_choices
    city_region_form.region.choices = city_region_choices

    street_form = StreetForm(request.form)
    street_form.city.choices = city_choices
    street_form.city_region.choices = city_region_choices

    new_building_form = NewBuildingForm(request.form)
    new_building_form.street.choices = street_choices
    new_building_form.region.choices = city_region_choices

    client_form = ClientForm(request.form)

    separation_form = SeparationForm(request.form)

    handbook_form = HandbookForm(request.form)

    if request.method == 'POST':
        if new_building_form.validate_on_submit():
            message = message_return(new_building_api.add(new_building_form.data))
            flash(message[0], message[1])
        elif client_form.validate_on_submit():
            message = message_return(client_api.add(client_form.data))
            flash(message[0], message[1])
        elif separation_form.validate_on_submit():
            message = message_return(separation_api.add(separation_form.data))
            flash(message[0], message[1])
        elif handbook_form.validate_on_submit():
            message = message_return(handbook_api.add(handbook_form.data))
            flash(message[0], message[1])
        elif street_form.validate_on_submit():
            message = message_return(street_api.add(street_form.data))
            flash(message[0], message[1])
        elif city_region_form.validate_on_submit():
            message = message_return(city_region_api.add(city_region_form.data))
            flash(message[0], message[1])
        elif city_form.validate_on_submit():
            message = message_return(city_api.add(city_form.data))
            flash(message[0], message[1])
        elif region_form.validate_on_submit():
            message = message_return(region_api.add(region_form.data))
            flash(message[0], message[1])
        elif district_form.validate_on_submit():
            message = message_return(district_api.add(district_form.data))
            flash(message[0], message[1])
    rights = check_user_rights(session.get("token"), ["catalog", "handbook", "main",
                                                      "add_handbook", "add_object", "all_types"])
    return render_template("add_handbook.html", district_form=district_form,
                           region_form=region_form, city_form=city_form,
                           city_region_form=city_region_form, street_form=street_form,
                           handbook_form=handbook_form, new_building_form=new_building_form,
                           separation_form=separation_form, client_form=client_form,
                           logged=user_logged(session.get("token")), rights=rights)


@app.route("/handbook/<string:table>/<int:post_id>", methods=['POST', 'GET'])
def change_handbook(table, post_id):
    if not auth_api.check_user_right(session.get("token"), "change_handbook"):
        return "403 Error Forbidden"
    if table == "districts":
        district = district_api.get(post_id)
        if district.get("detail"):
            return district.get("detail")
        form = DistrictForm(request.form)
        if request.method == "POST":
            form = DistrictForm(request.form)
            if form.validate_on_submit():
                message = district_api.refactor(post_id, form.data)
                if isinstance(message, dict):
                    flash(message.get("detail"), "danger")
                else:
                    flash(message, "success")
                    return redirect("/handbook/1")
            else:
                flash("Не все поля заполнены", "danger")

        form.district.data = district.get("district")

    elif table == 'regions':
        region = region_api.get(post_id)
        form = RegionForm(request.form)
        districts = district_api.get_all()
        form.district.choices = [(district.get("id"), district.get("district")) for district in districts]

        if request.method == "POST":
            if form.validate_on_submit():
                message = region_api.refactor(post_id, form.data)
                if isinstance(message, dict):
                    flash(message.get("detail"), "danger")
                else:
                    flash(message, "success")
                    return redirect("/handbook/1")
            else:
                flash("Не все поля запонены", "danger")

        form.region.data = region.get("region")
        selected_district = district_api.get(region.get("district"))
        form.district.data = (region.get("district"), selected_district.get("district"))

    elif table == 'cities':
        city = city_api.get(post_id)
        form = CityForm(request.form)
        form.region.choices = [(d.get("id"), d.get("region")) for d in region_api.get_all()]
        form.city_type.choices = [("село", "село"), ("смт", "смт"), ("місто", "місто")]
        form.center_type.choices = [("районний", "районний"), ("обласний", "обласний"), (None, None)]

        if request.method == "POST":
            if form.validate_on_submit():
                message = city_api.refactor(post_id, form.data)
                if isinstance(message, dict):
                    flash(message.get("detail"), "danger")
                else:
                    flash(message, "success")
                    return redirect("/handbook/1")
            else:
                flash("Не все поля запонены", "danger")

        selected_region = region_api.get(city.get("region"))
        form.city.data = city.get("city")
        form.region.data = (city.get("region"), selected_region.get("region"))
        form.city_type.data = (city.get("city_type"), city.get("city_type"))
        form.center_type.data = (city.get("center_type"), city.get("center_type"))

    elif table == 'city_regions':
        city_region = city_region_api.get(post_id)
        form = CityRegionForm(request.form)
        form.region.choices = [(region.get("id"), region.get("city_region")) for region in city_region_api.get_all()]
        form.region.choices.append((None, None))
        form.city.choices = [(city.get("id"), city.get("city")) for city in city_api.get_all()]
        form.new_building_region.choices = [("Приморский+Центр", "Приморский+Центр"),
                                            ("Киевский+Малиновский", "Киевский+Малиновский"),
                                            ("Суворовский", "Суворовский"), (None, None)]

        if request.method == "POST":
            if form.validate_on_submit():
                if form.region.data == "None":
                    form.region.data = None
                message = city_region_api.refactor(post_id, form.data)
                if isinstance(message, dict):
                    flash(message.get("detail"), "danger")
                else:
                    flash(message, "success")
                    return redirect("/handbook/1")
            else:
                flash("Не все поля запонены", "danger")

        selected_region = city_region_api.get(city_region.get("region"))
        if isinstance(selected_region, dict) and selected_region.get("detail"):
            selected_region = {"id": None, "city_region": None}
        selected_city = city_api.get(city_region.get("city"))
        form.city_region.data = city_region.get("city_region")
        form.description.data = city_region.get("description")
        form.group_on_site.data = city_region.get("group_on_site")
        form.hot_deals_limit.data = city_region.get("hot_deals_limit")
        form.prefix_to_site.data = city_region.get("prefix_to_site")
        form.is_subdistrict.data = city_region.get("is_subdistrict")
        form.region.data = (selected_region.get("id"), selected_region.get("city_region"))
        form.city.data = (city_region.get("city"), selected_city.get("city"))
        form.new_building_region.data = (city_region.get("new_building_region"), city_region.get("new_building_region"))
    elif table == 'streets':
        street = street_api.get(post_id)
        form = StreetForm()

        form.city_region.choices = [(region.get("id"), region.get("city_region")) for region in
                                    city_region_api.get_all()]
        form.city.choices = [(city.get("id"), city.get("city")) for city in city_api.get_all()]

        if request.method == "POST":
            if form.validate_on_submit():
                form = StreetForm(request.form)
                message = street_api.refactor(post_id, form.data)
                if isinstance(message, dict):
                    flash(message.get("detail"), "danger")
                else:
                    flash(message, "success")
                    return redirect("/handbook/1")
            else:
                flash("Не все поля запонены", "danger")

        selected_city_region = city_region_api.get(street.get("city_region"))
        selected_city = city_api.get(street.get("city"))
        form.street.data = street.get("street")
        form.city_region.data = (street.get("city_region"), selected_city_region.get("city_region"))
        form.city.data = (street.get("city"), selected_city.get("city"))
    elif table == 'handbooks':
        hb = handbook_api.get(post_id)  # handbook
        form = HandbookForm()

        if request.method == "POST":
            if form.validate_on_submit():
                form = HandbookForm(request.form)
                message = handbook_api.refactor(post_id, form.data)
                if isinstance(message, dict):
                    flash(message.get("detail"), "danger")
                else:
                    flash(message, "success")
                    return redirect("/handbook/1")

        form.handbook.data = hb.get("handbook")
        form.handbook_type.data = (hb.get("handbook_type"), hb.get("handbook_type"))
    elif table == "new_buildings":
        new_building = new_building_api.get(post_id)
        form = NewBuildingForm()
        form.street.choices = [(street.get("id"), street.get("street")) for street in street_api.get_all()]
        form.region.choices = [(city_region.get("id"),
                                city_region.get("city_region")) for city_region in city_region_api.get_all()]

        if request.method == "POST":
            if form.validate_on_submit():
                form = NewBuildingForm(request.form)
                message = new_building_api.refactor(post_id, form.data)
                if isinstance(message, dict):
                    flash(message.get("detail"), "danger")
                else:
                    flash(message, "success")
                    return redirect("/handbook/1")

        form.new_building.data = new_building.get("new_building")
        form.building.data = new_building.get("building")
        form.street.data = new_building.get("street")
        form.house.data = new_building.get("house")
        form.region.data = new_building.get("region")
    elif table == "separations":
        separation = separation_api.get(post_id)
        form = SeparationForm()

        if request.method == "POST":
            if form.validate_on_submit():
                form = SeparationForm(request.form)
                message = separation_api.refactor(post_id, form.data)
                if isinstance(message, dict):
                    flash(message.get("detail"), "danger")
                else:
                    flash(message, "success")
                    return redirect("/handbook/1")
        form.separation.data = separation.get("separation")
    elif table == "clients":
        client = client_api.get(post_id)
        form = ClientForm()

        if request.method == "POST":
            if form.validate_on_submit():
                form = ClientForm(request.form)
                message = client_api.refactor(post_id, form.data)
                if isinstance(message, dict):
                    flash(message.get("detail"), "danger")
                else:
                    flash(message, "success")
                    return redirect("/handbook/1")

        form.email.data = client.get("email")
        form.first_name.data = client.get("first_name")
        form.last_name.data = client.get("last_name")
        form.phone.data = client.get("phone")
    else:
        return "404 Error Not Found Handbook"
    rights = check_user_rights(session.get("token"), ["catalog", "handbook", "main",
                                                      "add_handbook", "add_object", "all_types"])
    return render_template("change_handbook.html", form=form,
                           logged=user_logged(session.get("token")), rights=rights)


@app.route("/handbook/delete/<string:table>/<int:post_id>")
def delete_handbook(table, post_id):
    if not auth_api.check_user_right(session.get("token"), "delete_handbook"):
        return "403 Error Forbidden"
    if table == "handbooks":
        message = message_return(handbook_api.delete(post_id))
        flash(message[0], message[1])
    elif table == "streets":
        message = message_return(street_api.delete(post_id))
        flash(message[0], message[1])
    elif table == "city_regions":
        message = message_return(city_region_api.delete(post_id))
        flash(message[0], message[1])
    elif table == "cities":
        message = message_return(city_api.delete(post_id))
        flash(message[0], message[1])
    elif table == "regions":
        message = message_return(region_api.delete(post_id))
        flash(message[0], message[1])
    elif table == "districts":
        message = message_return(district_api.delete(post_id))
        flash(message[0], message[1])
    elif table == "new_buildings":
        message = message_return(new_building_api.delete(post_id))
        flash(message[0], message[1])
    elif table == "separations":
        message = message_return(separation_api.delete(post_id))
        flash(message[0], message[1])
    elif table == "clients":
        message = message_return(client_api.delete(post_id))
        flash(message[0], message[1])
    else:
        flash("404 Error Not Found Handbook", "danger")
    return redirect("/handbook/1")


@app.route("/catalog/add/", methods=['POST', 'GET'])
def add_object():
    if not auth_api.check_user_right(session.get("token"), "add_object"):
        return "403 Error Forbidden"
    form = ObjectsForm(request.form)
    form.district.choices = [(district.get("id"), district.get("district")) for district in district_api.get_all()]
    form.region.choices = [(region.get("id"), region.get("region")) for region in region_api.get_all()]
    form.city.choices = city_api.get_all()
    form.city.choices = [(city.get("id"), city.get("city")) for city in city_api.get_all()]
    form.city_region.choices = city_region_api.get_all()
    form.city_region.choices = [(city_region.get("id"), city_region.get("city_region")) for city_region in
                                city_region_api.get_all()]
    form.street.choices = [(street.get("id"), street.get("street")) for street in street_api.get_all()]
    form.withdrawal_reason.choices = [(withdrawal_reason.get("id"), withdrawal_reason.get("handbook"))
                                      for withdrawal_reason
                                      in handbook_api.get_all("withdrawal_reason")] + [(None, None)]
    form.material.choices = [(material.get("id"), material.get("handbook"))
                             for material in handbook_api.get_all("material")]
    form.condition.choices = [(condition.get("id"), condition.get("handbook"))
                              for condition in handbook_api.get_all("condition")]
    form.object_type.choices = [(obj_type.get("id"), obj_type.get("type")) for obj_type in catalog_api.get_all()]
    form.owner.choices = [(owner.get("id"), f"{owner.get('first_name')} {owner.get('first_name')}"
                                            f" ({owner.get('email')})") for owner in client_api.get_all()]
    form.client.choices = [(client.get("id"), f"{client.get('first_name')} {client.get('first_name')}"
                                              f" ({client.get('email')})")
                           for client in client_api.get_all()] + [(None, None)]
    form.separation.choices = [(separation.get("id"), separation.get("separation"))
                               for separation in separation_api.get_all()]
    form.agency.choices = [(agency.get("id"), agency.get("handbook")) for agency in handbook_api.get_all("agency")]
    form.agency_sales.choices = [(agency.get("id"), agency.get("handbook"))
                                 for agency in handbook_api.get_all("agency")]
    form.new_building_name.choices = [(new_building.get("id"), new_building.get("new_building"))
                                      for new_building in new_building_api.get_all()] + [(None, None)]
    realtor_group = group_api.get_by_name("realtor")
    realtors = user_group_api.get_by_group(realtor_group.get("id"))
    users = []
    for realtor in realtors:
        users.append(auth_api.get(realtor.get("user")))
    realtor_choices = [(user.get("id"),
                        f"{user.get('first_name')} "
                        f"{user.get('last_name')} ({user.get('email')})") for user in users]
    form.realtor.choices = realtor_choices
    form.site_realtor1.choices = realtor_choices
    realtor_choices.append((None, None))
    form.site_realtor2.choices = realtor_choices
    form.realtor_5_5.choices = realtor_choices
    if request.method == "POST":
        if form.validate_on_submit():
            today = date.today()
            data = form.data
            data["date_before_temporarily_removed"] = date_refactor(data["date_before_temporarily_removed"])
            data["deposit_date"] = date_refactor(data["deposit_date"])
            data["purchase_date"] = date_refactor(data["purchase_date"])
            data["sale_date"] = date_refactor(data["sale_date"])
            data["date_of_next_call"] = date_refactor(data["date_of_next_call"])
            data["exclusive_to"] = date_refactor(data["exclusive_to"])
            data["exclusive_from"] = date_refactor(data["exclusive_from"])
            data.update({"create_date": today.strftime("%d.%m.%Y"),
                         "author": auth_api.get_current_user(session.get("token")).get("id")})
            message = message_return(object_api.add(data))
            flash(message[0], message[1])
        else:
            flash("Не все поля заполенны", "danger")
    rights = check_user_rights(session.get("token"), ["catalog", "handbook", "main",
                                                      "add_handbook", "add_object", "all_types"])
    return render_template("object.html", form=form, title="Добавление", image_add=False,
                           logged=user_logged(session.get("token")), rights=rights)


@app.route("/catalog/objects/<int:post_id>/", methods=['POST', 'GET'])
def change_object(post_id):
    if not auth_api.check_user_right(session.get("token"), "change_object"):
        return "403 Error Forbidden"
    obj = object_api.get(post_id)
    form = ObjectsForm(request.form)
    form.district.choices = [(district.get("id"), district.get("district")) for district in district_api.get_all()]
    form.region.choices = [(region.get("id"), region.get("region")) for region in region_api.get_all()]
    form.city.choices = city_api.get_all()
    form.city.choices = [(city.get("id"), city.get("city")) for city in city_api.get_all()]
    form.city_region.choices = city_region_api.get_all()
    form.city_region.choices = [(city_region.get("id"), city_region.get("city_region")) for city_region in
                                city_region_api.get_all()]
    form.street.choices = [(street.get("id"), street.get("street")) for street in street_api.get_all()]
    form.withdrawal_reason.choices = [(withdrawal_reason.get("id"), withdrawal_reason.get("handbook"))
                                      for withdrawal_reason
                                      in handbook_api.get_all("withdrawal_reason")] + [(None, None)]
    form.material.choices = [(material.get("id"), material.get("handbook"))
                             for material in handbook_api.get_all("material")]
    form.condition.choices = [(condition.get("id"), condition.get("handbook"))
                              for condition in handbook_api.get_all("condition")]
    form.object_type.choices = [(obj_type.get("id"), obj_type.get("type")) for obj_type in catalog_api.get_all()]
    form.owner.choices = [(owner.get("id"), f"{owner.get('first_name')} {owner.get('first_name')}"
                                            f" ({owner.get('email')})") for owner in client_api.get_all()]
    form.client.choices = [(client.get("id"), f"{client.get('first_name')} {client.get('first_name')}"
                                              f" ({client.get('email')})")
                           for client in client_api.get_all()] + [(None, None)]
    form.separation.choices = [(separation.get("id"), separation.get("separation"))
                               for separation in separation_api.get_all()]
    form.agency.choices = [(agency.get("id"), agency.get("handbook")) for agency in handbook_api.get_all("agency")]
    form.agency_sales.choices = [(agency.get("id"), agency.get("handbook"))
                                 for agency in handbook_api.get_all("agency")]
    form.new_building_name.choices = [(new_building.get("id"), new_building.get("new_building"))
                                      for new_building in new_building_api.get_all()] + [(None, None)]
    realtor_group = group_api.get_by_name("realtor")
    realtors = user_group_api.get_by_group(realtor_group.get("id"))
    users = []
    for realtor in realtors:
        users.append(auth_api.get(realtor.get("user")))
    realtor_choices = [(user.get("id"),
                        f"{user.get('first_name')} "
                        f"{user.get('last_name')} ({user.get('email')})") for user in users]
    form.realtor.choices = realtor_choices
    form.site_realtor1.choices = realtor_choices
    realtor_choices.append((None, None))
    form.site_realtor2.choices = realtor_choices
    form.realtor_5_5.choices = realtor_choices

    if request.method == 'POST':
        if "obj_image" in request.files:
            file = request.files["obj_image"]
            file_slug = file.filename.split('.')[-1]
            file.save(f'./img/image{post_id}.{file_slug}')
            files = {"img": open(f'./img/image{post_id}.{file_slug}', 'rb')}
            message = message_return(object_image_api.add(post_id, files=files))
            flash(message[0], message[1])
        elif request.form.get('id'):
            if request.form.get('on_site') == 'on':
                data = {"on_site": True}
            else:
                data = {"on_site": False}
            message = message_return(object_image_api.refactor(request.form.get('id'), data))
            flash(message[0], message[1])
        elif form.validate_on_submit():
            data = form.data
            data["date_before_temporarily_removed"] = date_refactor(data["date_before_temporarily_removed"])
            data["deposit_date"] = date_refactor(data["deposit_date"])
            data["purchase_date"] = date_refactor(data["purchase_date"])
            data["sale_date"] = date_refactor(data["sale_date"])
            data["date_of_next_call"] = date_refactor(data["date_of_next_call"])
            data["exclusive_to"] = date_refactor(data["exclusive_to"])
            data["exclusive_from"] = date_refactor(data["exclusive_from"])
            data.update({"create_date": obj.get("create_date"),
                         "author": obj.get("author")})
            message = object_api.refactor(post_id, data)
            if isinstance(message, dict):
                flash(message.get("detail"), "danger")
            else:
                flash("Объект обновлен", "success")
                return redirect(f"/catalog/{form.data['object_type']}/{post_id}")
        else:
            flash("Не все поля заполенны", "danger")

    form.date_before_temporarily_removed.data = obj.get("date_before_temporarily_removed")
    form.deposit_date.data = obj.get("deposit_date")
    form.purchase_date.data = obj.get("purchase_date")
    form.sale_date.data = obj.get("sale_date")
    form.date_of_next_call.data = obj.get("date_of_next_call")
    form.exclusive.data = obj.get("exclusive")
    form.exclusive_to.data = obj.get("exclusive_to")
    form.exclusive_from.data = obj.get("exclusive_from")
    form.district.data = obj.get("district")
    form.region.data = obj.get("region")
    form.city.data = obj.get("city")
    form.city_region.data = obj.get("city_region")
    form.street.data = obj.get("street")
    form.house.data = obj.get("house")
    form.apartment.data = obj.get("apartment")
    form.on_site.data = obj.get("on_site")
    form.inspection_flag.data = obj.get("inspection_flag")
    form.paid_exclusive_flag.data = obj.get("paid_exclusive_flag")
    form.terrace_flag.data = obj.get("terrace_flag")
    form.sea_flag.data = obj.get("sea_flag")
    form.vip.data = obj.get("vip")
    form.withdrawal_reason.data = obj.get("withdrawal_reason")
    form.independent.data = obj.get("independent")
    form.condition.data = obj.get("condition")
    form.special.data = obj.get("special")
    form.urgently.data = obj.get("urgently")
    form.trade.data = obj.get("trade")
    form.material.data = obj.get("material")
    form.status.data = obj.get("status")
    form.square.data = obj.get("square")
    form.price.data = obj.get("price")
    form.site_price.data = obj.get("site_price")
    form.square_meter_price.data = obj.get("square_meter_price")
    form.realtor.data = obj.get("realtor")
    form.site_realtor1.data = obj.get("site_realtor1")
    form.site_realtor2.data = obj.get("site_realtor2")
    form.realtor_5_5.data = obj.get("realtor_5_5")
    form.for_trainee.data = obj.get("for_trainee")
    form.realtor_notes.data = obj.get("realtor_notes")
    form.reference_point.data = obj.get("reference_point")
    form.owner.data = obj.get("owner")
    form.client.data = obj.get("client")
    form.owners_number.data = obj.get("owners_number")
    form.comment.data = obj.get("comment")
    form.separation.data = obj.get("separation")
    form.agency.data = obj.get("agency")
    form.agency_sales.data = obj.get("agency_sales")
    form.sale_terms.data = obj.get("sale_terms")
    form.filename_of_exclusive_agreement.data = obj.get("filename_of_exclusive_agreement")
    form.inspection_file_name.data = obj.get("inspection_file_name")
    form.document.data = obj.get("document")
    form.filename_forbid_sale.data = obj.get("filename_forbid_sale")
    form.new_building_name.data = obj.get("new_building_name")
    form.new_building.data = obj.get("new_building")
    form.new_building_type.data = obj.get("new_building_type")

    images = object_image_api.get_all_by_object(post_id)
    clear_images = []
    for image in images:
        img_form = UpdateObjectImageForm()
        img_form.id.data = image.get("id")
        img_form.on_site.data = image.get("on_site")
        clear_images.append([img_form, object_image_api.get_image(image.get("source"))])
    rights = check_user_rights(session.get("token"), ["catalog", "handbook", "main",
                                                      "add_handbook", "add_object", "all_types"])
    return render_template("object.html", form=form, images=clear_images,
                           title="Обновление", object_id=post_id, image_add=True,
                           logged=user_logged(session.get("token")), rights=rights)


@app.route("/catalog/<int:catalog_id>/<int:object_id>/inspection/")
def update_inspection_form(catalog_id, object_id):
    if not auth_api.check_user_right(session.get("token"), "update_details"):
        return "403 Error Forbidden"
    obj = object_api.get(object_id)
    obj_type = catalog_api.get(obj.get("object_type"))
    if catalog_id != obj_type.get("id"):
        return "404 Error Not Found Catalog Type"
    if obj_type.get("slug") == "apartments":
        obj["inspection_form"] = str(datetime.datetime.now())
        message = object_api.refactor(object_id, obj)
        if isinstance(message, dict):
            flash(message.get("detail"), "danger")
        else:
            flash("Объект обновлен", "success")
        return redirect(f"/catalog/{catalog_id}/{object_id}")


@app.route("/catalog/<int:catalog_id>/<int:object_id>/details/", methods=['POST', 'GET'])
def update_details(catalog_id, object_id):
    if not auth_api.check_user_right(session.get("token"), "update_details"):
        return "403 Error Forbidden"
    obj = object_api.get(object_id)
    obj_type = catalog_api.get(obj.get("object_type"))
    if catalog_id != obj_type.get("id"):
        return "404 Error Not Found Catalog Type"
    if obj_type.get("slug") == "apartments":
        form = ApartmentsForm(request.form)
        form.stair.choices = [(stair.get("id"), stair.get("handbook")) for stair in handbook_api.get_all("stair")]
        form.heating.choices = [(heating.get("id"), heating.get("handbook"))
                                for heating in handbook_api.get_all("heating")]
        form.layout.choices = [(layout.get("id"), layout.get("handbook")) for layout in handbook_api.get_all("layout")]
        form.house_type.choices = [(house_type.get("id"), house_type.get("handbook"))
                                   for house_type in handbook_api.get_all("house_type")]
        apartment = apartment_api.get_by_object(object_id)
        if request.method == 'POST':
            if form.validate_on_submit():
                data = form.data
                data.update({"object": object_id})
                if isinstance(apartment, dict) and apartment.get("detail"):
                    message = apartment_api.add(data)
                elif isinstance(apartment, dict) and apartment.get("id"):
                    message = apartment_api.refactor(apartment.get("id"), data)
                if isinstance(message, dict):
                    flash(message.get("detail"), "danger")
                else:
                    flash("Детали обновлены", "success")
                    return redirect(f"/catalog/{catalog_id}/{object_id}")
            else:
                flash("Не все поля заполнены", "danger")
        if isinstance(apartment, dict) and apartment.get("id"):
            form.rooms_number.data = apartment.get("rooms_number")
            form.room_types.data = apartment.get("room_types")
            form.height.data = apartment.get("height")
            form.kitchen_square.data = apartment.get("kitchen_square")
            form.living_square.data = apartment.get("living_square")
            form.gas.data = apartment.get("gas")
            form.courtyard.data = apartment.get("courtyard")
            form.balcony_number.data = apartment.get("balcony_number")
            form.registered_number.data = apartment.get("registered_number")
            form.child_registered_number.data = apartment.get("child_registered_number")
            form.loggias_number.data = apartment.get("loggias_number")
            form.bay_windows_number.data = apartment.get("bay_windows_number")
            form.commune.data = apartment.get("commune")
            form.frame.data = apartment.get("frame")
            form.stair.data = apartment.get("stair")
            form.balcony.data = apartment.get("balcony")
            form.heating.data = apartment.get("heating")
            form.office.data = apartment.get("office")
            form.penthouse.data = apartment.get("penthouse")
            form.redevelopment.data = apartment.get("redevelopment")
            form.layout.data = apartment.get("layout")
            form.construction_number.data = apartment.get("construction_number")
            form.house_type.data = apartment.get("house_type")
            form.two_level_apartment.data = apartment.get("two_level_apartment")
            form.loggia.data = apartment.get("loggia")
            form.attic.data = apartment.get("attic")
            form.electric_stove.data = apartment.get("electric_stove")
            form.floor.data = apartment.get("floor")
            form.storeys_number.data = apartment.get("storeys_number")
        rights = check_user_rights(session.get("token"), ["catalog", "handbook", "main",
                                                          "add_handbook", "add_object", "all_types"])
        return render_template("object.html", form=form,
                               title="Обновление", object_id=object_id, image_add=False,
                               logged=user_logged(session.get("token")), rights=rights)
    else:
        return "404 Error Not Found Object Details"


@app.route("/catalog/delete/<int:object_id>/<int:image_id>/")
def delete_object_image(object_id, image_id):
    if not auth_api.check_user_right(session.get("token"), "delete_object_image"):
        return "403 Error Forbidden"
    message = message_return(object_image_api.delete(image_id))
    flash(message[0], message[1])
    return redirect(f"/catalog/objects/{object_id}/")


@app.route("/catalog/delete/<int:post_id>/")
def delete_object(post_id):
    if not auth_api.check_user_right(session.get("token"), "delete_object"):
        return "403 Error Forbidden"
    message = object_api.delete(post_id)
    if isinstance(message, dict):
        flash(message.get("detail"), "danger")
    else:
        flash(message, "success")
    return redirect(f"/catalog/")


@app.route("/types/")
def all_types():
    if not auth_api.check_user_right(session.get("token"), "all_types"):
        return "403 Error Forbidden"
    types = catalog_api.get_all()
    rights = check_user_rights(session.get("token"), ["catalog", "handbook", "main", "add_handbook",
                                                      "add_object", "change_type", "delete_type", "all_types"])
    return render_template("types.html", types=types,
                           logged=user_logged(session.get("token")), rights=rights)


@app.route("/types/<int:type_id>", methods=['POST', 'GET'])
def change_type(type_id):
    if not auth_api.check_user_right(session.get("token"), "change_type"):
        return "403 Error Forbidden"
    catalog_type = catalog_api.get(type_id)
    form = ObjectTypeForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            message = catalog_api.refactor(type_id, form.data)
            if isinstance(message, dict):
                flash(message.get("detail"), "danger")
            else:
                flash(message, "success")
                return redirect(f"/types")
    form.type.data = catalog_type.get("type")
    rights = check_user_rights(session.get("token"), ["catalog", "handbook", "main",
                                                      "add_handbook", "add_object", "all_types"])
    return render_template("change_type.html", form=form,
                           logged=user_logged(session.get("token")), rights=rights)


@app.route("/types/delete/<int:type_id>")
def delete_types(type_id):
    if not auth_api.check_user_right(session.get("token"), "delete_type"):
        return "403 Error Forbidden"
    message = catalog_api.delete(type_id)
    if isinstance(message, dict):
        flash(message.get("detail"), "danger")
    else:
        flash(message, "success")
    return redirect(f"/types")


@app.route("/about/")
def about():
    return render_template('about.html')


@app.route("/contacts/")
def contacts():
    return render_template('contacts.html')


@app.route("/login/", methods=['POST', 'GET'])
def login():
    register = Register(request.form)
    auth = Authorization(request.form)
    if request.method == "POST":
        if register.validate_on_submit():
            message = auth_api.create_new_user(register.data)
            if isinstance(message, dict):
                flash(message.get("detail"), "danger")
            else:
                group = group_api.get_by_name("user")
                data = {"user": message, "group": group.get("id")}
                user_group_api.add(data)
                flash("Вы зарегестрировались! Теперь войдите!", "success")
                return redirect("/login/#undefined1")
        elif auth.validate_on_submit():
            message = auth_api.login_for_access_token({"password": auth.password.data, "email": auth.email.data})
            if isinstance(message, dict) and message.get("token"):
                session["token"] = message.get("token")
                flash("Вы вошли!", "success")
                return redirect("/")
            else:
                flash(message.get("detail"), "danger")
    rights = check_user_rights(session.get("token"), ["catalog", "handbook", "main", "add_handbook", "add_object"])
    return render_template('login.html', register=register, auth=auth,
                           logged=user_logged(session.get("token")), rights=rights)


@app.route("/logout")
def logout():
    session.pop("token")
    flash("Вы вышли!", "success")
    return redirect("/")


@app.route("/privacy/")
def privacy():
    return render_template('privacy.html')


@app.route("/services/")
def services():
    return render_template('services.html')


@app.route("/submit/")
def submit():
    return render_template('submit-property.html')


@app.route("/team_member/")
def team_member():
    return render_template('team-member.html')


if __name__ == '__main__':
    app.run()
