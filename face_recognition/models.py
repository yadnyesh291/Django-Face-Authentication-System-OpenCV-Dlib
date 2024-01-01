from django.db import models

class UserProfile (models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=100)
    username = models.CharField(max_length=110)
    password = models.CharField(max_length=110)
    # Add a field to store face encodings as a binary blob
    face_encoding = models.BinaryField(null=True, blank=True)
    REQUIRED_FIELDS=[]
    # def _str_(self):
    # return {self.name}, {self.email}, {self.username}


