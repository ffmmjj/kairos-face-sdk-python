import requests
import base64
from kairos_face import exceptions, validate_settings, validate_file_and_url_presence
from kairos_face import settings

_detect_base_url = settings.base_url + 'detect'


def detect_face(url=None, file=None, additional_arguments={}):
    validate_settings()
    validate_file_and_url_presence(file, url)

    auth_headers = {
        'app_id': settings.app_id,
        'app_key': settings.app_key
    }
    payload = _build_payload(url, file, additional_arguments)

    response = requests.post(_detect_base_url, json=payload, headers=auth_headers)
    json_response = response.json()
    if response.status_code != 200 or 'Errors' in json_response:
        raise exceptions.ServiceRequestError(response.status_code, json_response, payload)

    return json_response


def _build_payload(url, file, additional_arguments):
    if file is not None:
        image = _extract_base64_contents(file)
    else:
        image = url

    required_fields = {
        'image': image
    }

    return dict(required_fields, **additional_arguments)


def _extract_base64_contents(image_path):
    with open(image_path, 'rb') as fp:
        return base64.b64encode(fp.read()).decode('ascii')
