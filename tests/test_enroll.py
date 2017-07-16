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
            kairos_face.enroll_face('sub_id', 'gallery', url='a_image_path.jpg')

    def test_throws_exception_when_app_key_is_not_set(self):
        kairos_face.settings.app_key = None

        with self.assertRaises(kairos_face.SettingsNotPresentException):
            kairos_face.enroll_face('sub_id', 'gallery', url='a_image_path.jpg')

    def test_throws_exception_when_url_is_empty_string(self):
        with self.assertRaises(ValueError):
            kairos_face.enroll_face('subject_id', 'gallery', url='')

    def test_throws_exception_when_file_is_empty_string(self):
        with self.assertRaises(ValueError):
            kairos_face.enroll_face('subject_id', 'gallery', file='')

    def test_throws_exception_when_both_file_and_url_are_passed(self):
        with self.assertRaises(ValueError):
            kairos_face.enroll_face('subject_id', 'gallery',
                                    url='an_image_url.jpg', file='/path/tp/image.jpg')

    def test_throws_exception_when_both_file_and_imgframe_are_passed(self):
        with self.assertRaises(ValueError):
            kairos_face.enroll_face('subject_id', 'gallery',
                                    url='an_image_url.jpg', base64_image_contents='aBase64EncodedImageContents')

    @mock.patch('kairos_face.requests.post')
    def test_passes_api_url_in_post_request(self, post_mock):
        post_mock.return_value.status_code = 200

        kairos_face.enroll_face('sub_id', 'gallery', url='image')

        args, _ = post_mock.call_args
        self.assertEqual(1, len(args), 'No positional arguments were passed to post request')
        self.assertEqual('https://api.kairos.com/enroll', args[0])

    @mock.patch('kairos_face.requests.post')
    def test_passes_app_id_and_key_in_post_header(self, post_mock):
        post_mock.return_value.status_code = 200

        kairos_face.enroll_face('sub_id', 'gallery', url='a_image_url.jpg')

        _, kwargs = post_mock.call_args
        expected_headers = {
            'app_id': 'app_id',
            'app_key': 'app_key'
        }
        self.assertTrue('headers' in kwargs)
        self.assertEqual(expected_headers, kwargs['headers'])

    @mock.patch('kairos_face.requests.post')
    def test_passes_required_arguments_in_payload_as_json_when_image_is_url(self, post_mock):
        post_mock.return_value.status_code = 200

        kairos_face.enroll_face('sub_id', 'gallery', url='a_image_url.jpg')

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
    def test_passes_required_arguments_in_payload_as_json_when_image_is_file(self, post_mock):
        post_mock.return_value.status_code = 200

        m = mock.mock_open(read_data=str.encode('test'))
        with mock.patch('builtins.open', m, create=True):
            kairos_face.enroll_face('sub_id', 'gallery', file='/a/image/file.jpg')

        _, kwargs = post_mock.call_args
        expected_payload = {
            'image': 'dGVzdA==',
            'subject_id': 'sub_id',
            'gallery_name': 'gallery',
            'multiple_faces': False
        }
        self.assertTrue('json' in kwargs)
        self.assertEqual(expected_payload, kwargs['json'])

    @mock.patch('kairos_face.requests.post')
    def test_passes_multiple_faces_argument_in_payload_when_flag_is_set(self, post_mock):
        post_mock.return_value.status_code = 200

        m = mock.mock_open(read_data=str.encode('test'))
        with mock.patch('builtins.open', m, create=True):
            kairos_face.enroll_face('sub_id', 'gallery', file='/a/image/file.jpg', multiple_faces=True)

        _, kwargs = post_mock.call_args
        expected_payload = {
            'image': 'dGVzdA==',
            'subject_id': 'sub_id',
            'gallery_name': 'gallery',
            'multiple_faces': True
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

        kairos_face.enroll_face('sub_id', 'gallery',
                                url='a_image_url.jpg', additional_arguments=additional_arguments)

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
            kairos_face.enroll_face('sub_id', 'gallery', url='a_image_url.jpg')

    @responses.activate
    def test_raises_exception_when_http_response_body_contains_error_field(self):
        response_body = '{"Errors": "something something dark side..."}'
        responses.add(responses.POST, 'https://api.kairos.com/enroll', status=200,
                      body=response_body)

        with self.assertRaises(kairos_face.ServiceRequestError):
            kairos_face.enroll_face('sub_id', 'gallery', url='a_image_url.jpg')

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

        actual_response = kairos_face.enroll_face('sub_id', 'gallery', url='a_image_url.jpg')

        self.assertEqual('new_face_id', actual_response['images'][0]['transaction']['face_id'])

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

        actual_response = kairos_face.enroll_face('sub_id', 'gallery', url='a_image_url.jpg')

        expected_attributes = {
            'gender': {
                'type': 'F',
                'confidence': '80%'
            }
        }
        self.assertEqual(expected_attributes, actual_response['images'][0]['attributes'])
