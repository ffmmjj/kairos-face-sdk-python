from kairos_face import exceptions
from kairos_face import settings
import requests
import base64
from io import BufferedReader
from functools import singledispatch

from kairos_face.entities import RecognizedFaceCandidate

_recognize_base_url = settings.base_url + 'recognize'


def recognize_face(image, gallery_name, additional_arguments={}):
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

    first_image = json_response['images'][0]
    recognized_faces = []
    if first_image['transaction']['status'] != 'failure':
        recognized_faces.append(_subject_from_first_response(first_image))
        recognized_faces.extend(_extract_candidates(first_image['candidates'][1:]))

    return recognized_faces


def _subject_from_first_response(first_response):
    return RecognizedFaceCandidate(
        first_response['transaction']['subject'],
        float(first_response['transaction']['confidence'])
    )


def _extract_candidates(candidates_dict_array):
    candidates = []
    for entry in candidates_dict_array:
        entry.pop('enrollment_timestamp')
        subject_name = list(entry.keys())[0]
        candidates.append(RecognizedFaceCandidate(subject_name, float(entry[subject_name])))

    return sorted(candidates, key=lambda c: c.confidence)


def _flatten(candidate_keys):
    return [val for sublist in candidate_keys for val in sublist]


def _build_payload(gallery_name, image, additional_arguments):
    required_fields = {
        'image': _image_representation(image),
        'gallery_name': gallery_name
    }

    return dict(required_fields, **additional_arguments)


@singledispatch
def _image_representation(image):
    raise TypeError('Expected image to be a string or BufferedReader, received {}'.format(type(image)))


@_image_representation.register(str)
def _with_string(image):
    return image


@_image_representation.register(BufferedReader)
def _with_bytes_stream(image):
    return base64.b64encode(image.read()).decode('ascii')


def _validate_settings():
    if settings.app_id is None:
        raise exceptions.SettingsNotPresentException("Kairos app_id was not set")
    if settings.app_key is None:
        raise exceptions.SettingsNotPresentException("Kairos app_key was not set")
