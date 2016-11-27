# kairos-face-sdk-python
Kairos Face Recognition API Python Client Library

## Installation
`pip install .` inside the project root directory

## Usage
### Setting up the API keys
The library exposes a *settings* object where the API keys can be set. It should be remarked that the API keys **must be set before** any of the library's functions is used:

```python
import kairos_face

kairos_face.settings.app_id = <your_app_id_here>
kairos_face.settings.app_key = <your_app_key_here>
```

Your API keys can be found in your Kairo's admin dashboard.

## Enrolling new faces
A face can be enrolled by passing an image URL or file:

```python
import kairos_face

# Enrolling from a URL
kairos_face.enroll_face(url='http://some.server/some-image.jpg', subject_id='subject1', gallery_name='a-gallery')

# Enrolling from a file
kairos_face.enroll_face(file=image_file, subject_id='subject1', gallery_name='a-gallery')
```

## Detect a face
The API can detect a face from a image passed as an URL or a file. 

```python
import kairos_face

# Detect from an URL
recognized_faces = kairos_face.detect_face(url='http://some.server/some-image.jpg', gallery_name='a-gallery')

# Detect from a file
recognized_faces = kairos_face.detect_face(file=local_image_file, gallery_name='a-gallery')
```

## Recognizing a face
The API can identify a face in an existing gallery from a image passed as an URL or a file. 

```python
import kairos_face

# Recognizing from an URL
recognized_faces = kairos_face.recognize_face(url='http://some.server/some-image.jpg', gallery_name='a-gallery')

# Recognizing from a file
recognized_faces = kairos_face.recognize_face(file=local_image_file, gallery_name='a-gallery')
```
## Verify a face
The API can verify that a face belongs to a specific person in an existing gallery from a image passed as an URL or a file. 

```python
import kairos_face

# Verify from an URL
recognized_faces = kairos_face.verify_face(url='http://some.server/some-image.jpg', gallery_name='a-gallery')

# Verify from a file
recognized_faces = kairos_face.verify_face(file=local_image_file, gallery_name='a-gallery')
```

## Galleries
Face subjects are grouped in galleries. 

#### Get Galleries
List all galleries that have been created.

```python
import kairos_face

galleries_list = kairos_face.get_galleries_names_list()
```

#### Get Gallery
Get a list of subjects in a specific gallery.

```python
import kairos_face

gallery_subjects = kairos_face.get_gallery('a-gallery')
```

#### Remove Gallery
Remove a gallery and all its subjects.

```python
import kairos_face

remove_gallery = kairos_face.remove_gallery('a-gallery')
```

There are special methods which combine to render each gallery, followed by a list of subjects enrolled in that gallery:

```python
import kairos_face

galleries_object = kairos_face.get_galleries_names_object()

for gallery_name in galleries_object:
    gallery = kairos_face.get_gallery_object(gallery_name)
    print('Gallery name: {}'.format(gallery.name))
    print('Gallery subjects: {}'.format(gallery.subjects))
```

## Removing an enrolled face
Previously enrolled faces can be removed from a gallery:

```python
import kairos_face

kairos_face.remove_face(subject_id='subject1', gallery_name='a-gallery')
```

