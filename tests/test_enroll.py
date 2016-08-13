import json
import unittest
from unittest import mock
import responses

import kairos_face


class KairosApiEnrollFacesTest(unittest.TestCase):
    def setUp(self):
        kairos_face.settings.app_id = 'app_id'
        kairos_face.settings.app_key = 'app_key'

    def test_throws_exception_when_app_id_is_not_set(self):
        kairos_face.settings.app_id = None

        with self.assertRaises(kairos_face.SettingsNotPresentException):
            kairos_face.enroll_face('a_image_path.jpg', subject_id='sub_id', gallery_name='gallery')

    def test_throws_exception_when_app_key_is_not_set(self):
        kairos_face.settings.app_key = None

        with self.assertRaises(kairos_face.SettingsNotPresentException):
            kairos_face.enroll_face('a_image_path.jpg', subject_id='sub_id', gallery_name='gallery')

    def test_throws_exception_when_image_is_empty_string(self):
        with self.assertRaises(ValueError):
            kairos_face.enroll_face('', subject_id='subject_id', gallery_name='gallery')

    @mock.patch('kairos_face.requests.post')
    def test_passes_image_url_in_post_header(self, post_mock):
        post_mock.return_value.status_code = 200

        kairos_face.enroll_face('image', subject_id='sub_id', gallery_name='gallery')

        args, _ = post_mock.call_args
        self.assertEqual(1, len(args), 'No positional arguments were passed to post request')
        self.assertEqual('https://api.kairos.com/enroll', args[0])

    @mock.patch('kairos_face.requests.post')
    def test_passes_app_id_and_key_in_post_header(self, post_mock):
        post_mock.return_value.status_code = 200

        kairos_face.enroll_face('a_image_url.jpg', subject_id='sub_id', gallery_name='gallery')

        _, kwargs = post_mock.call_args
        expected_headers = {
            'app_id': 'app_id',
            'app_key': 'app_key'
        }
        self.assertTrue('headers' in kwargs)
        self.assertEqual(expected_headers, kwargs['headers'])

    @mock.patch('kairos_face.requests.post')
    def test_passes_required_arguments_in_payload_as_json(self, post_mock):
        post_mock.return_value.status_code = 200

        kairos_face.enroll_face('a_image_url.jpg', subject_id='sub_id', gallery_name='gallery')

        _, kwargs = post_mock.call_args
        expected_payload = {
            'image': 'a_image_url.jpg',
            'subject_id': 'sub_id',
            'gallery_name': 'gallery',
            'multiple_faces': False
        }
        self.assertTrue('json' in kwargs)
        self.assertEqual(expected_payload, kwargs['json'])

    @mock.patch('kairos_face.requests.post')
    def test_passes_additional_arguments_in_payload(self, post_mock):
        post_mock.return_value.status_code = 200
        additional_arguments = {
            'selector': 'SETPOSE',
            'symmetricFill': True
        }

        kairos_face.enroll_face('a_image_url.jpg', subject_id='sub_id', gallery_name='gallery',
                                additional_arguments=additional_arguments)

        _, kwargs = post_mock.call_args
        passed_payload = kwargs['json']
        self.assertTrue('selector' in passed_payload)
        self.assertEqual('SETPOSE', passed_payload['selector'])
        self.assertTrue('symmetricFill' in passed_payload)
        self.assertEqual(True, passed_payload['symmetricFill'])

    @responses.activate
    def test_raises_exception_when_http_status_response_is_error(self):
        response_body = '{"error_message": "something something dark side..."}'
        responses.add(responses.POST, 'https://api.kairos.com/enroll', status=400,
                      body=response_body)

        with self.assertRaises(kairos_face.ServiceRequestError):
            kairos_face.enroll_face('a_image_url.jpg', subject_id='sub_id', gallery_name='gallery')

    @responses.activate
    def test_raises_exception_when_http_response_body_contains_error_field(self):
        response_body = '{"Errors": "something something dark side..."}'
        responses.add(responses.POST, 'https://api.kairos.com/enroll', status=200,
                      body=response_body)

        with self.assertRaises(kairos_face.ServiceRequestError):
            kairos_face.enroll_face('a_image_url.jpg', subject_id='sub_id', gallery_name='gallery')

    @responses.activate
    def test_returns_face_id_from_kairos_response(self):
        response_dict = {
            'images': [{
                'transaction': {'face_id': 'new_face_id'},
                'attributes': {}
            }]
        }
        responses.add(responses.POST, 'https://api.kairos.com/enroll', status=200,
                      body=(json.dumps(response_dict)))

        face_id, _ = kairos_face.enroll_face('a_image_url.jpg', subject_id='sub_id', gallery_name='gallery')

        self.assertEqual('new_face_id', face_id)

    @responses.activate
    def test_returns_image_attributes_from_kairos_response(self):
        response_dict = {
            'images': [{
                'transaction': {'face_id': 'new_face_id'},
                'attributes': {
                    'gender': {'type': 'F', 'confidence': '80%'}
                }
            }]
        }
        responses.add(responses.POST, 'https://api.kairos.com/enroll', status=200,
                      body=json.dumps(response_dict))

        _, attributes = kairos_face.enroll_face('a_image_url.jpg', subject_id='sub_id', gallery_name='gallery')

        expected_attributes = {
            'gender': {
                'type': 'F',
                'confidence': 0.8
            }
        }
        self.assertEqual(expected_attributes, attributes)