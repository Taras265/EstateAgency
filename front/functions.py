from api.all_api import *


def get_object_detail(obj: dict):
    images = object_image_api.get_by_object(obj.get("id"))
    if images:
        image_name = images[0].get("source")
    else:
        image_name = "default.jpg"
    if len(images) > 1:
        clean_images = []
        images = images[1::]
        for img in images:
            clean_images.append(f"{OBJECT_IMAGES_URL}/{img['source']}")
    else:
        clean_images = None
    data = obj.copy()
    data.update({"image_source": f"{OBJECT_IMAGES_URL}/{image_name}", "image_sources": clean_images})
    data["id"] = obj.get("id")
    data["withdrawal_reason"] = handbook_api.get(obj.get("withdrawal_reason")).get("handbook")
    data["condition"] = handbook_api.get(obj.get("condition")).get("handbook")
    data["material"] = handbook_api.get(obj.get("material")).get("handbook")
    data["realtor"] = auth_api.get(obj.get("realtor"))
    data["site_realtor1"] = auth_api.get(obj.get("site_realtor1"))
    data["site_realtor2"] = auth_api.get(obj.get("site_realtor2"))
    data["realtor_5_5"] = auth_api.get(obj.get("realtor_5_5"))
    data["owner"] = client_api.get(obj.get("owner"))
    data["client"] = client_api.get(obj.get("client"))
    data["separation"] = separation_api.get(obj.get("separation")).get("separation")
    data["agency"] = handbook_api.get(obj.get("agency")).get("handbook")
    data["agency_sales"] = handbook_api.get(obj.get("agency_sales")).get("handbook")
    data["new_building_name"] = new_building_api.get(obj.get("new_building")).get("handbook")
    data["address"] = locations_api.get_address([data["district"], data["region"], data["city"],
                                                 data["city_region"], data["street"],
                                                 data["house"], data["apartment"]])
    return data


def get_objects_details(objects):
    objects_detail = []
    for obj in objects:
        objects_detail.append(get_object_detail(obj))
    return objects_detail


def user_logged(token):
    user = auth_api.get_current_user(token)
    if not user.get("email") or not user.get("id"):
        return False
    return True


def check_user_rights(token: str, rights: list):
    data = {}
    for right in rights:
        user_right = auth_api.check_user_right(token, right)
        data.update({right: user_right})
    return data


def message_return(message):
    if isinstance(message, dict) and message.get("detail"):
        return message.get("detail"), "danger"
    else:
        return message, "success"


def handbook_sort(api, api_list: dict, on_page):
    if len(api_list) == 2:
        data_dict = api.get_on_page(api_list[0], api_list[1])
    else:
        data_dict = api.get_on_page(api_list[0], api_list[1], api_list[2])
    data = data_dict.get("objects")
    data_pages = data_dict.get("count") or 0
    data_pages /= on_page
    if str(data_pages)[-2::] != ".0":
        data_pages += 1
    data_pages = int(data_pages)
    if data_pages == 0:
        data_pages = 1
    return data_dict, data, data_pages


def handbook_pages(obj_name, objects: list, keys: list, api: dict, page, max_pages):
    for num in range(0, len(objects)):
        for key in keys:
            objects[num][key] = api[key].get(objects[num].get(key)).get(key)
    data = {obj_name: objects}
    data.update(standard_pages(page, max_pages))
    return data


def standard_pages(page, max_pages):
    if page > max_pages:
        object_page = max_pages
    else:
        object_page = page
    if page <= 1:
        prev_page = max_pages
    else:
        prev_page = object_page - 1
    if page >= max_pages:
        next_page = 1
    else:
        next_page = object_page + 1
    return {"next": next_page, "prev": prev_page, "page": object_page}


def date_refactor(date):
    if date:
        return str(date)
    return date
