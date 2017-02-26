import requests

from kairos_face import exceptions, validate_settings
from kairos_face import settings
from kairos_face.entities import KairosFaceGallery

_gallery_base_url = settings.base_url + 'gallery/view'
_galleries_list_url = settings.base_url + 'gallery/list_all'
_gallery_remove_url = settings.base_url + 'gallery/remove'


def get_gallery(gallery_name):
    validate_settings()
    _validate_gallery_name(gallery_name)

    auth_headers = {
        'app_id': settings.app_id,
        'app_key': settings.app_key
    }

    payload = {'gallery_name': gallery_name}
    response = requests.post(_gallery_base_url, json=payload, headers=auth_headers)
    json_response = response.json()
    if response.status_code != 200 or 'Errors' in json_response:
        raise exceptions.ServiceRequestError(response.status_code, json_response, payload)

    return response.json()


def get_galleries_names_list():
    validate_settings()

    auth_headers = {
        'app_id': settings.app_id,
        'app_key': settings.app_key
    }

    response = requests.post(_galleries_list_url, headers=auth_headers)
    json_response = response.json()
    if response.status_code != 200 or 'Errors' in json_response:
        raise exceptions.ServiceRequestError(response.status_code, json_response, None)

    return json_response


def remove_gallery(gallery_name):
    validate_settings()
    _validate_gallery_name(gallery_name)

    auth_headers = {
        'app_id': settings.app_id,
        'app_key': settings.app_key
    }

    payload = {'gallery_name': gallery_name}

    response = requests.post(_gallery_remove_url, json=payload, headers=auth_headers)
    json_response = response.json()
    if response.status_code != 200 or 'Errors' in json_response:
        raise exceptions.ServiceRequestError(response.status_code, json_response, payload)

    return json_response


def get_galleries_names_object():
    validate_settings()

    auth_headers = {
        'app_id': settings.app_id,
        'app_key': settings.app_key
    }

    response = requests.post(_galleries_list_url, headers=auth_headers)
    json_response = response.json()
    if response.status_code != 200 or 'Errors' in json_response:
        raise exceptions.ServiceRequestError(response.status_code, json_response, None)

    return json_response['gallery_ids']


def get_gallery_object(gallery_name):
    validate_settings()
    _validate_gallery_name(gallery_name)

    auth_headers = {
        'app_id': settings.app_id,
        'app_key': settings.app_key
    }

    payload = {'gallery_name': gallery_name}
    response = requests.post(_gallery_base_url, json=payload, headers=auth_headers)
    json_response = response.json()
    if response.status_code != 200 or 'Errors' in json_response:
        raise exceptions.ServiceRequestError(response.status_code, json_response, payload)

    return KairosFaceGallery(gallery_name, json_response['subject_ids'])


def _validate_gallery_name(gallery_name):
    if not gallery_name:
        raise ValueError("gallery_name cannot be empty")
