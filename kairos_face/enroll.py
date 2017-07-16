import base64

import requests

from kairos_face import exceptions
from kairos_face import settings
from kairos_face.utils import validate_file_and_url_presence, validate_settings

_enroll_base_url = settings.base_url + 'enroll'


def enroll_face(subject_id, gallery_name,
                url=None, file=None, base64_image_contents=None,
                multiple_faces=False, additional_arguments={}):
    validate_settings()
    validate_file_and_url_presence(file, url)

    auth_headers = {
        'app_id': settings.app_id,
        'app_key': settings.app_key
    }

    payload = _build_payload(subject_id, gallery_name, url, file,
                             base64_image_contents, multiple_faces, additional_arguments)

    response = requests.post(_enroll_base_url, json=payload, headers=auth_headers)
    json_response = response.json()
    if response.status_code != 200 or 'Errors' in json_response:
        raise exceptions.ServiceRequestError(response.status_code, json_response, payload)

    return json_response


def _build_payload(subject_id, gallery_name, url, file, imgframe, multiple_faces, additional_arguments):
    if imgframe is not None:
        image = imgframe
    elif file is not None:
        image = _extract_base64_contents(file)
    else:
        image = url
    required_fields = {'image': image, 'subject_id': subject_id,
                       'gallery_name': gallery_name, 'multiple_faces': multiple_faces}

    return dict(required_fields, **additional_arguments)


def _extract_base64_contents(file):
    with open(file, 'rb') as fp:
        image = base64.b64encode(fp.read()).decode('ascii')
    return image
