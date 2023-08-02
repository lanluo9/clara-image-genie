from django.db import models

## 3 steps to make model changes:
# Change your models (in clara/models.py).
# Run python manage.py makemigrations to create migrations for those changes
# Run python manage.py migrate to apply those changes to the database.

### tutorial models
class Question(models.Model):
    def __str__(self):
        return self.question_text
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


class Choice(models.Model):
    def __str__(self):
        return self.question_text
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
    def __str__(self):
        return self.keyword + ' in ' + self.folder_path + ' using ' + self.search_mode
    folder_path = models.CharField(max_length=200)
    keyword = models.CharField(max_length=200)
    search_mode = models.CharField(max_length=50)


class Result(models.Model):
    '''contains:
    absolute path to picture [str]
    image content [str]
    content extraction mode [str]: object detection, image description, OCR. match search mode
    '''
    def __str__(self):
        return self.img_content + ' in ' + self.img_path + ' using ' + self.content_extraction_mode
    img_path = models.CharField(max_length=200)
    img_content = models.CharField(max_length=200)
    content_extraction_mode = models.CharField(max_length=50)
    # TODO: add snippet_keyword field to store the snippet of img_content that contains the keyword
    # query = models.ForeignKey(Query, on_delete=models.CASCADE)


