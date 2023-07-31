from django.db import models

### tutorial models
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


### my models
class Query(models.Model):
    '''contains: 
    absolute path to folder (picture album to search) [str]
    search keyword [str]
    search mode [str]: object detection, image description, OCR
    '''
    folder_path = models.CharField(max_length=200)
    keyword = models.CharField(max_length=200)
    search_mode = models.CharField(max_length=50)


class Result(models.Model):
    '''contains:
    absolute path to picture [str]
    image content [str]
    content extraction mode [str]: object detection, image description, OCR. match search mode
    '''
    picture_path = models.CharField(max_length=200)
    content = models.CharField(max_length=200)
    content_extraction_mode = models.CharField(max_length=50)
    # query = models.ForeignKey(Query, on_delete=models.CASCADE)


