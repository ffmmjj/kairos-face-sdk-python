from kairos_face import settings, exceptions


def validate_file_and_url_presence(file, url):
    if not file and not url:
        raise ValueError('An image file or valid URL must be passed')
    if file and url:
        raise ValueError('Cannot receive both a file and URL as arguments')


def validate_settings():
    if settings.app_id is None:
        raise exceptions.SettingsNotPresentException('Kairos app_id was not set')
    if settings.app_key is None:
        raise exceptions.SettingsNotPresentException('Kairos app_key was not set')
