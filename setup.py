# from distutils.core import setup
from setuptools import setup


setup(
    name='kairos_face_recognition_lib',
    version='0.3.0',
    packages=['kairos_face'],
    url='https://github.com/ffmmjj/kairos-face-sdk-python',
    license='MIT',
    author='Felipe Martins',
    author_email='',
    description='Kairos Face Recognition API Python Client Library',
    install_requires=[
        'requests'
    ]
)
