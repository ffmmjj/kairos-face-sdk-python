# kairos-face-sdk-python
Kairos Face Recognition API Python Client Library

## Installation
`pip install .` inside the project root directory

## Usage
### Enrolling new faces
A face can be enrolled by passing an image URL or file:

```python
import kairos_face

# Enrolling from a URL
kairos_face.enroll_face('http://some.server/some-image.jpg', subject_id='subject1', gallery_name='a-gallery')

# Enrolling from a file
with open('path/to/a/file.jpg', 'rb') as image_file:
    kairos_face.enroll_face(image_file, subject_id='subject1', subject_id='subject1', gallery_name='a-gallery')
```

### Recognizing a face
The API can identify a face from a image passed as an URL or a file. The function returns a list of **RecognizedFaceCandidate** instances, each one having a subject ID and a confidence level:

```python
import kairos_face

# Recognizing from an URL
recognized_faces = kairos_face.recognize_face('http://some.server/some-image.jpg', gallery_name='a-gallery')

# Enrolling from a file
with open('path/to/a/file.jpg', 'rb') as image_file:
    recognized_faces = kairos_face.recognize_face('http://some.server/some-image.jpg', gallery_name='a-gallery')

# Printing the recognized face candidates info
for face_candidate in recognized_faces:
    print('{}: {}'.format(face_candidate.subject, face_candidate.confidence)
```

### Galleries
Face subjects are grouped in galleries. A list of the current galleries' names can be retrieved by calling **get_galleries_names_list()**.
Individual galleries can be retrieved by passing their names to **get_gallery()** and each gallery has a list of the subjects that were enrolled to them:

```python
import kairos_face

galleries_list = kairos_face.get_galleries_names_list()

for gallery_name in galleries_list:
    gallery = kairos_face.get_gallery(gallery_name)
    print('Gallery name: {}'.format(gallery.name))
    print('Gallery subjects: {}'.format(gallery.subjects))
```

### Removing an enrolled face
Previously enrolled faces can be removed from a gallery:

```python
import kairos_face

kairos_face.remove_face(subject_id='subject1', gallery_name='a-gallery')
```
