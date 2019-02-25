from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Attachment(models.Model):
    file = models.FileField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='attachments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'File {self.file}'


class Question(models.Model):
    text = models.CharField('question text', max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='questions', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    attachmetns = GenericRelation(Attachment)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.TextField('answer text')
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='answers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    attachments = GenericRelation(Attachment)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return f'Question {self.question_id}: {self.text}'


class Theme(models.Model):
    title = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='themes', on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='following_themes')

    def __str__(self):
        return self.title


class Like(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'Like created at {self.created_at}'
