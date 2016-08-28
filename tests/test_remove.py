import unittest
import responses

import kairos_face


class KairosApiRemoveFaceTest(unittest.TestCase):
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

    def test_throws_exception_when_subject_id_is_empty_string(self):
        with self.assertRaises(ValueError):
            kairos_face.remove_face(subject_id='', gallery_name='gallery')

    def test_throws_exception_when_gallery_name_is_empty_string(self):
        with self.assertRaises(ValueError):
            kairos_face.remove_face(subject_id='sub_id', gallery_name='')

    @responses.activate
    def test_remove_face_that_does_not_exist_raises_exception(self):
        response_body = '{"Errors":[{"ErrCode":5003,"Message":"subject id was not found"}]}'
        responses.add(responses.POST, 'https://api.kairos.com/gallery/remove_subject',
                      status=200,
                      body=response_body)

        with self.assertRaises(kairos_face.ServiceRequestError):
            kairos_face.remove_face(gallery_name='gallery_name', subject_id='non_existing_face')

    @responses.activate
    def test_remove_existing_face_returns_success_payload(self):
        response_body = """
        {
            "status": "Complete",
            "message": "subject id integration-test-face2 has been successfully removed"
        }
        """
        responses.add(responses.POST, 'https://api.kairos.com/gallery/remove_subject',
                      status=200,
                      body=response_body)

        response = kairos_face.remove_face(gallery_name='gallery_name', subject_id='existing_face')

        self.assertEqual("Complete", response['status'])
        self.assertTrue('message' in response)
