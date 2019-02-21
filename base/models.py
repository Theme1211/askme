from django.conf import settings
from django.db import models


class Question(models.Model):
    text = models.CharField('question text', max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='questions', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.TextField('answer text')
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='answers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return f'Question {self.question_id}: {self.text}'


class Theme(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='themes', on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='following_themes')
