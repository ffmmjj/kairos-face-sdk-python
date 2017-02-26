import json
import unittest
import responses
from unittest import mock

import kairos_face


class KairosApiGalleryTest(unittest.TestCase):
    def setUp(self):
        kairos_face.settings.app_id = 'app_id'
        kairos_face.settings.app_key = 'app_key'

    def test_throws_exception_when_app_id_is_not_set(self):
        kairos_face.settings.app_id = None

        with self.assertRaises(kairos_face.SettingsNotPresentException):
            kairos_face.get_gallery(gallery_name='gallery')

    def test_throws_exception_when_app_key_is_not_set(self):
        kairos_face.settings.app_key = None

        with self.assertRaises(kairos_face.SettingsNotPresentException):
            kairos_face.get_gallery(gallery_name='gallery')

    @mock.patch('kairos_face.requests.post')
    def test_passes_app_id_and_key_in_post_header(self, post_mock):
        post_mock.return_value.status_code = 200

        kairos_face.get_gallery(gallery_name='gallery')

        _, kwargs = post_mock.call_args
        expected_headers = {
            'app_id': 'app_id',
            'app_key': 'app_key'
        }
        self.assertTrue('headers' in kwargs)
        self.assertEqual(expected_headers, kwargs['headers'])

    @mock.patch('kairos_face.requests.post')
    def test_payload_with_gallery_name_is_passed_in_request(self, post_mock):
        post_mock.return_value.status_code = 200

        kairos_face.get_gallery(gallery_name='gallery')

        _, kwargs = post_mock.call_args
        expected_payload = {
            'gallery_name': 'gallery'
        }
        self.assertTrue('json' in kwargs)
        self.assertEqual(expected_payload, kwargs['json'])

    @responses.activate
    def test_getting_non_existing_gallery_raises_an_exception(self):
        response_body = {"Errors": [{"ErrCode": 5004, "Message": "gallery name not found"}]}
        responses.add(responses.POST, 'https://api.kairos.com/gallery/view',
                      status=200,
                      body=json.dumps(response_body))

        with self.assertRaises(kairos_face.ServiceRequestError):
            kairos_face.get_gallery('non-existing-gallery')

    @responses.activate
    def test_returned_gallery_has_face_subjects_list(self):
        response_body = {
              "time": 0.00991,
              "status": "Complete",
              "subject_ids": [
                "subject1",
                "subject2",
                "subject3"
              ]
        }
        responses.add(responses.POST, 'https://api.kairos.com/gallery/view',
                      status=200,
                      body=json.dumps(response_body))

        actual_response = kairos_face.get_gallery('a-gallery')

        self.assertEqual('Complete', actual_response['status'])
        self.assertEqual(3, len(actual_response['subject_ids']))
        self.assertTrue('subject1' in actual_response['subject_ids'])
        self.assertTrue('subject2' in actual_response['subject_ids'])
        self.assertTrue('subject3' in actual_response['subject_ids'])


class KairosApiGetGalleriesListTest(unittest.TestCase):
    def setUp(self):
        kairos_face.settings.app_id = 'app_id'
        kairos_face.settings.app_key = 'app_key'

    def test_throws_exception_when_app_id_is_not_set(self):
        kairos_face.settings.app_id = None

        with self.assertRaises(kairos_face.SettingsNotPresentException):
            kairos_face.get_galleries_names_list()

    def test_throws_exception_when_app_key_is_not_set(self):
        kairos_face.settings.app_key = None

        with self.assertRaises(kairos_face.SettingsNotPresentException):
            kairos_face.get_galleries_names_list()

    @responses.activate
    def test_returns_empty_list_when_no_galleries_are_present(self):
        response_body = {
            "time": 0.00991,
            "status": "Complete",
            "gallery_ids": []
        }
        responses.add(responses.POST, 'https://api.kairos.com/gallery/list_all',
                      status=200,
                      body=json.dumps(response_body))

        actual_response = kairos_face.get_galleries_names_list()

        self.assertEqual(0, len(actual_response['gallery_ids']))

    @responses.activate
    def test_returns_available_galleries_names(self):
        response_body = {
            "time": 0.00991,
            "status": "Complete",
            "gallery_ids": [
                'gallery1',
                'gallery2'
            ]
        }
        responses.add(responses.POST, 'https://api.kairos.com/gallery/list_all',
                      status=200,
                      body=json.dumps(response_body))

        actual_response = kairos_face.get_galleries_names_list()

        self.assertEquals('Complete', actual_response['status'])
        self.assertEqual(2, len(actual_response['gallery_ids']))
        self.assertTrue('gallery1' in actual_response['gallery_ids'])
        self.assertTrue('gallery2' in actual_response['gallery_ids'])
