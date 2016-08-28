import requests

from kairos_face import exceptions, validate_settings
from kairos_face import settings
from kairos_face.entities import KairosFaceGallery

_gallery_base_url = settings.base_url + 'gallery/view'
_galleries_list_url = settings.base_url + 'gallery/list_all'


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

    return KairosFaceGallery(gallery_name, json_response['subject_ids'])


def get_galleries_names_list():
    _validate_settings()

    auth_headers = {
        'app_id': settings.app_id,
        'app_key': settings.app_key
    }

    response = requests.post(_galleries_list_url, headers=auth_headers)
    json_response = response.json()
    if response.status_code != 200 or 'Errors' in json_response:
        raise exceptions.ServiceRequestError(response.status_code, json_response, None)

    return json_response['gallery_ids']


def _validate_gallery_name(gallery_name):
    if not gallery_name:
        raise ValueError("gallery_name cannot be empty")


def _validate_settings():
    if settings.app_id is None:
        raise exceptions.SettingsNotPresentException("Kairos app_id was not set")
    if settings.app_key is None:
        raise exceptions.SettingsNotPresentException("Kairos app_key was not set")
