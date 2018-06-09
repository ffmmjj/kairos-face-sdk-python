import traceback

import kairos_face
import os
import unittest

from kairos_face.exceptions import ServiceRequestError


class EnrollIntegrationTest(unittest.TestCase):
    def setUp(self):
        # It was not possible to find a reliable, publicly available URL pointing to a face picture
        # with nice quality.
        # To avoid legal issues, you'l have to set up your own ;)
        self.face_example_url = os.environ.get('EXAMPLE_FACE_URL')

    def test_image_response_is_returned(self):
        try:
            response = kairos_face.enroll_face(
                'integration-test-face',
                'integration-test-gallery',
                url=self.face_example_url
            )

            self.assertIsNotNone(response['face_id'])
            self.assertEqual('M', response['images'][0]['attributes']['gender']['type'])
        except ServiceRequestError:
            traceback.print_exc()
            self.fail('This should not be raising an exception...')
        finally:
            kairos_face.remove_face(subject_id='integration-test-face',
                                    gallery_name='integration-test-gallery')
