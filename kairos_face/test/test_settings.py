import unittest


class KairosApiSettingsTest(unittest.TestCase):
    def test_api_initializes_settings_as_none(self):
        import kairos_face

        self.assertIsNone(kairos_face.settings.app_id)
        self.assertIsNone(kairos_face.settings.app_key)
