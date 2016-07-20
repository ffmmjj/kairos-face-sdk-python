from kairos_face import exceptions
from kairos_face import settings
import requests

_recognize_base_url = settings.base_url + 'recognize'


def recognize_face(gallery_name, image, additional_arguments={}):
    _validate_settings()
    auth_headers = {
        'app_id': settings.app_id,
        'app_key': settings.app_key
    }
    payload = _build_payload(gallery_name, image, additional_arguments)

    response = requests.post(_recognize_base_url, json=payload, headers=auth_headers)
    json_response = response.json()
    if response.status_code != 200 or 'Errors' in json_response:
        raise exceptions.ServiceRequestError(response.status_code, json_response, payload)

    first_response = json_response['images'][0]
    if first_response['transaction']['status'] == 'failure':
        return _empty_response()

    return {
        'recognized_subject': first_response['transaction']['subject'],
        'candidates': _extract_candidates(first_response['candidates'])
    }


def _empty_response():
    return {
        'recognized_subject': None,
        'candidates': []
    }


def _extract_candidates(candidates_dict_array):
    candidate_keys = _flatten([[k for k in c.keys()] for c in candidates_dict_array])
    return list(set(candidate_keys) - {'enrollment_timestamp'})


def _flatten(candidate_keys):
    return [val for sublist in candidate_keys for val in sublist]


def _build_payload(gallery_name, image, additional_arguments):
    required_fields = {
        'image': image,
        'gallery_name': gallery_name
    }

    return dict(required_fields, **additional_arguments)


def _validate_settings():
    if settings.app_id is None:
        raise exceptions.SettingsNotPresentException("Kairos app_id was not set")
    if settings.app_key is None:
        raise exceptions.SettingsNotPresentException("Kairos app_key was not set")