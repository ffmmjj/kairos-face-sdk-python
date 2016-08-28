import base64

from kairos_face import exceptions
from kairos_face import settings
import requests

_enroll_base_url = settings.base_url + 'enroll'


def enroll_face(subject_id, gallery_name, url=None, file=None, additional_arguments={}):
    _validate_arguments(file, url)
    auth_headers = {
        'app_id': settings.app_id,
        'app_key': settings.app_key
    }

    payload = _build_payload(subject_id, gallery_name, url, file, additional_arguments)

    response = requests.post(_enroll_base_url, json=payload, headers=auth_headers)
    json_response = response.json()
    if response.status_code != 200 or 'Errors' in json_response:
        raise exceptions.ServiceRequestError(response.status_code, json_response, payload)

    image_response = json_response['images'][0]
    return image_response['transaction']['face_id'], _normalize_attributes(image_response['attributes'])


def _normalize_attributes(raw_attributes):
    return {k: _normalize_confidence(v) for k, v in raw_attributes.items()}


def _normalize_confidence(attribute_fields):
    normalized_attributes = dict(attribute_fields)
    normalized_attributes['confidence'] = _percentage_string_to_number(normalized_attributes['confidence'])

    return normalized_attributes


def _percentage_string_to_number(confidence_string):
    return float(confidence_string.replace('%', '')) / 100.0


def _build_payload(subject_id, gallery_name, url, file, additional_arguments):
    if file is not None:
        image = _extract_base64_contents(file)
    else:
        image = url
    required_fields = {'image': image, 'subject_id': subject_id,
                       'gallery_name': gallery_name, 'multiple_faces': False}

    return dict(required_fields, **additional_arguments)


def _extract_base64_contents(file):
    with open(file, 'rb') as fp:
        image = base64.b64encode(fp.read()).decode('ascii')
    return image


def _validate_arguments(file, url):
    if settings.app_id is None:
        raise exceptions.SettingsNotPresentException('Kairos app_id was not set')
    if settings.app_key is None:
        raise exceptions.SettingsNotPresentException('Kairos app_key was not set')
    if not file and not url:
        raise ValueError('An image file or valid URL must be passed')
    if file and url:
        raise ValueError('Cannot receive both a file and URL as arguments')
