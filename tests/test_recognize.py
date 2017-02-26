import json
import unittest
from io import BufferedReader
from unittest import mock

import responses

import kairos_face


class KairosApiRecognizeFaceTest(unittest.TestCase):
    def setUp(self):
        kairos_face.settings.app_id = 'app_id'
        kairos_face.settings.app_key = 'app_key'

    def test_throws_exception_when_app_id_is_not_set(self):
        kairos_face.settings.app_id = None

        with self.assertRaises(kairos_face.SettingsNotPresentException):
            kairos_face.recognize_face('gallery', url='an_image_url.jpg')

    def test_throws_exception_when_app_key_is_not_set(self):
        kairos_face.settings.app_key = None

        with self.assertRaises(kairos_face.SettingsNotPresentException):
            kairos_face.recognize_face('gallery', url='an_image_url.jpg')

    def test_throws_exception_when_url_is_empty_string(self):
        with self.assertRaises(ValueError):
            kairos_face.recognize_face('gallery', url='')

    def test_throws_exception_when_file_is_empty_string(self):
        with self.assertRaises(ValueError):
            kairos_face.recognize_face('gallery', file='')

    def test_throws_exception_when_both_file_and_url_are_passed(self):
        with self.assertRaises(ValueError):
            kairos_face.recognize_face('gallery', url='an_image_url.jpg', file='/path/tp/image.jpg')

    @mock.patch('kairos_face.requests.post')
    def test_passes_required_arguments_in_payload_as_json_when_image_is_file(self, post_mock):
        post_mock.return_value.status_code = 200

        with mock.patch('builtins.open', mock.mock_open(read_data=str.encode('test'))):
            with open('/a/image/file.jpg', 'rb') as image_file:
                image_file.__class__ = BufferedReader
                kairos_face.recognize_face('gallery', file=image_file)

        _, kwargs = post_mock.call_args
        expected_payload = {
            'image': 'dGVzdA==',
            'gallery_name': 'gallery'
        }
        self.assertTrue('json' in kwargs)
        self.assertEqual(expected_payload, kwargs['json'])

    @mock.patch('kairos_face.requests.post')
    def test_passes_additional_arguments_in_payload(self, post_mock):
        post_mock.return_value.status_code = 200
        additional_arguments = {
            'max_num_results': '5',
            'selector': 'EYES'
        }

        kairos_face.recognize_face('gallery', url='an_image_url.jpg',
                                   additional_arguments=additional_arguments)

        _, kwargs = post_mock.call_args
        passed_payload = kwargs['json']
        self.assertTrue('max_num_results' in passed_payload)
        self.assertEqual('5', passed_payload['max_num_results'])
        self.assertTrue('selector' in passed_payload)
        self.assertEqual('EYES', passed_payload['selector'])

    @responses.activate
    def test_returns_matching_images(self):
        response_body = {
            "images": [
                {
                    "time": 2.86091,
                    "transaction":
                    {
                        "status": "Complete",
                        "subject": "test2",
                        "confidence": "0.802138030529022",
                        "gallery_name": "gallerytest1",
                    },
                    "candidates": [
                        {
                          "test2": "0.802138030529022",
                          "enrollment_timestamp": "1416850761"
                        },
                        {
                          "elizabeth": "0.602138030529022",
                          "enrollment_timestamp": "1417207485"
                        }
                    ]
                }
            ]
        }
        responses.add(responses.POST, 'https://api.kairos.com/recognize',
                      status=200,
                      body=json.dumps(response_body))

        face_candidates_subjects = kairos_face.recognize_face('gallery_name', url='an_image_url.jpg')

        self.assertEqual(2, len(face_candidates_subjects['images'][0]['candidates']))

        image_response = face_candidates_subjects['images'][0]
        self.assertEquals('Complete', image_response['transaction']['status'])

        candidates = image_response['candidates']
        self.assertEquals(2, len(candidates))
        self.assertIn('test2', candidates[0])
        self.assertIn('0.802138030529022', candidates[0].values())
        self.assertIn('elizabeth', candidates[1])
        self.assertIn('0.602138030529022', candidates[1].values())

    @responses.activate
    def test_returns_transaction_failure_when_face_is_not_recognized(self):
        response_body = {
            "images": [{
                    "time": 6.43752,
                    "transaction": {
                            "status": "failure",
                            "message": "No match found",
                            "gallery_name": "gallery_name"
                        },
                    }]
                }
        responses.add(responses.POST, 'https://api.kairos.com/recognize',
                      status=200,
                      body=json.dumps(response_body))

        face_candidates_subjects = kairos_face.recognize_face('gallery_name', url='an_image_url.jpg')

        self.assertEquals(1, len(face_candidates_subjects['images']))

        image_response = face_candidates_subjects['images'][0]
        self.assertEquals('failure', image_response['transaction']['status'])
        self.assertEquals('No match found', image_response['transaction']['message'])
