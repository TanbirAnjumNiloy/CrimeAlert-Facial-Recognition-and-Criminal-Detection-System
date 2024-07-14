from django.db import models
import numpy as np
#-----------------------------------------------------------Library--------------------------------------------------------------#






#-----------------------------------------------------------Img Storage Database--------------------------------------------------------------#

from django.db import models
import numpy as np

class ImageUpload(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='uploads/')
    details = models.TextField()
    face_encoding = models.BinaryField(null=True)

    def __str__(self):
        return self.name

    def save_face_encodings(self, encoding):
        self.face_encoding = np.array(encoding).tobytes()
        self.save()

    def get_face_encodings(self):
        if self.face_encoding:
            encoding_array = np.frombuffer(self.face_encoding, dtype=np.float64)
            return [encoding_array]
        return []

#-----------------------------------------------------------Img Storage Database--------------------------------------------------------------#