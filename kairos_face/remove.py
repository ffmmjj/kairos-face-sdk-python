from kairos_face import exceptions
from kairos_face import settings
import requests

_remove_base_url = settings.base_url + 'gallery/remove_subject'


def remove_face(subject_id, gallery_name):
    _validate_settings()
    auth_headers = {
        'app_id': settings.app_id,
        'app_key': settings.app_key
    }

    payload = _build_payload(gallery_name, subject_id)

    response = requests.post(_remove_base_url, json=payload, headers=auth_headers)
    json_response = response.json()
    if response.status_code != 200 or 'Errors' in json_response:
        raise exceptions.ServiceRequestError(response.status_code, json_response, payload)

    return json_response


def _build_payload(gallery_name, subject_id):
    return {
        'gallery_name': gallery_name,
        'subject_id': subject_id
    }


def _validate_settings():
    if settings.app_id is None:
        raise exceptions.SettingsNotPresentException("Kairos app_id was not set")
    if settings.app_key is None:
        raise exceptions.SettingsNotPresentException("Kairos app_key was not set")
