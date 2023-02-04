from django.db import models

# # Create your models here.
#class Suggestion(models.Model):
#    user_relationship = models.CharField(max_length=200)
#     occasion = models.CharField(max_length=200)
#     user_interests = models.CharField(max_length=200)
#     user_budget = models.CharField(max_length=200)
#     user_abilities = models.CharField(max_length=200)
#     suggestion = models.TextField()

#from django.db import models

class Image(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    
    def __str__(self):
        return self.title