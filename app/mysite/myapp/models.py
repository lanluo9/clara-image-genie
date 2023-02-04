from django.db import models

class Image(models.Model):
    file_name = models.CharField(max_length=100)
    file_path = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.file_name