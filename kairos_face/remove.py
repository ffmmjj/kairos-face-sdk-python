from kairos_face import exceptions, validate_settings
from kairos_face import settings
import requests

_remove_base_url = settings.base_url + 'gallery/remove_subject'


def remove_face(subject_id, gallery_name):
    validate_settings()
    _validate_arguments_presence(gallery_name, subject_id)

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


def _validate_arguments_presence(gallery_name, subject_id):
    if not subject_id:
        raise ValueError('A subject ID must be passed')
    if not gallery_name:
        raise ValueError('A gallery name must be passed')


def _build_payload(gallery_name, subject_id):
    return {
        'gallery_name': gallery_name,
        'subject_id': subject_id
    }
