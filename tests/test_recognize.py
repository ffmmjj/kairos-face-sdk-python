import json
import unittest
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
            kairos_face.remove_face(subject_id='sub_id', gallery_name='gallery')

    def test_throws_exception_when_app_key_is_not_set(self):
        kairos_face.settings.app_key = None

        with self.assertRaises(kairos_face.SettingsNotPresentException):
            kairos_face.remove_face(subject_id='sub_id', gallery_name='gallery')

    @mock.patch('kairos_face.requests.post')
    def test_passes_additional_arguments_in_payload(self, post_mock):
        post_mock.return_value.status_code = 200
        additional_arguments = {
            'max_num_results': '5',
            'selector': 'EYES'
        }

        kairos_face.recognize_face(gallery_name='gallery', image='a_image_url.jpg',
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
                        "confidence": 0.77,
                        "gallery_name": "gallerytest1",
                    },
                    "candidates": [
                        {
                          "subtest1": "0.802138030529022",
                          "enrollment_timestamp": "1416850761"
                        },
                        {
                          "elizabeth": "0.802138030529022",
                          "enrollment_timestamp": "1417207485"
                        }
                    ]
                }
            ]
        }
        responses.add(responses.POST, 'https://api.kairos.com/recognize',
                      status=200,
                      body=json.dumps(response_body))

        response = kairos_face.recognize_face(gallery_name='gallery_name', image='an_image_path.jpg')

        self.assertEqual('test2', response['recognized_subject'])
        self.assertEqual(2, len(response['candidates']))
        self.assertTrue('subtest1' in response['candidates'])
        self.assertTrue('elizabeth'in response['candidates'])

    @responses.activate
    def test_raises_exception_when_face_is_not_recognized(self):
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

        response = kairos_face.recognize_face(gallery_name='gallery_name', image='an_image_path.jpg')

        self.assertIsNone(response['recognized_subject'])
        self.assertEqual(0, len(response['candidates']))
