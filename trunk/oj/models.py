# -*- coding: utf8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ProblemSet(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.name

class Problem(models.Model):
    CUSTOM_JUDGE_TYPE_CHOICES = (
        (0, u'None'),
        (1, u'C Code'),
    )
    
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    hint = models.TextField(null=True, blank=True)
    input_format = models.TextField()
    output_format = models.TextField()
    input_sample = models.TextField()
    output_sample = models.TextField()
    input_judge = models.TextField()
    output_judge = models.TextField()
    time_limit = models.IntegerField()
    memory_limit = models.IntegerField()
    custom_judge_type = models.IntegerField(choices=CUSTOM_JUDGE_TYPE_CHOICES, default=0)
    custom_judge_code = models.TextField(null=True, blank=True)
    author = models.ForeignKey(User, null=True, blank=True, related_name='authored_problems', on_delete=models.SET_NULL)
    problem_set = models.ForeignKey(ProblemSet, null=True, blank=True, related_name='problems')
    source = models.CharField(max_length=100, null=True, blank=True)
    source_url = models.URLField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

class ProblemAttribute(models.Model):
    problem = models.ForeignKey(Problem, related_name='attributes')
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=255)
    
class Comment(models.Model):
    author = models.ForeignKey(User, related_name='comments')
    time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True, on_delete=models.SET_NULL)
    problem = models.ForeignKey(Problem, related_name='comments')
    agreement = models.IntegerField(default=0)
    disagreement = models.IntegerField(default=0)
    
class CommentAttachment(models.Model):
    comment = models.ForeignKey(Comment, related_name='attachments')
    file = models.FileField(upload_to='attachments')
    filename = models.CharField(max_length=255)
    size = models.IntegerField()

class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    intro = models.TextField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(User, related_name='teams')
    
class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)
    short_name = models.CharField(max_length=50, unique=True)
    time_mul = models.FloatField(default=1.0)
    memory_mul = models.FloatField(default=1.0)
    extensions = models.CharField(max_length=255)
    
class Contest(models.Model):
    TYPE_CHOICES = (
        (0, u'Personal Contest'),
        (1, u'Team Contest'),
    )
    OPEN_CHOICES = (
        (0, u'Private'),
        (1, u'Public'),
        (2, u'Password'),
    )
    
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    type = models.IntegerField(choices=TYPE_CHOICES)
    open = models.IntegerField(choices=OPEN_CHOICES, default=0)
    password = models.CharField(max_length=100, null=True, blank=True)
    need_approve = models.BooleanField(default=True)
    problems = models.ManyToManyField(Problem, related_name='contests')
    languages = models.ManyToManyField(Language, related_name='+')
    
class ContestUser(models.Model):
    APPROVED_CHOICES = (
        (0, u'Pending'),
        (1, u'Approved'),
        (2, u'Denied'),
    )
    
    contest = models.ForeignKey(Contest, related_name='contest_users')
    user = models.ForeignKey(User, related_name='user_contests')
    join_time = models.DateTimeField(auto_now_add=True)
    approved = models.IntegerField(choices=APPROVED_CHOICES, default=0)

class ContestTeam(models.Model):
    APPROVED_CHOICES = (
        (0, u'Pending'),
        (1, u'Approved'),
        (2, u'Denied'),
    )
    
    contest = models.ForeignKey(Contest, related_name='contest_teams')
    team = models.ForeignKey(Team, related_name='team_contests')
    join_time = models.DateTimeField(auto_now_add=True)
    approved = models.IntegerField(choices=APPROVED_CHOICES, default=0)
    
class Submission(models.Model):
    STATUS_CHOICES = (
        (0, u'Queueing'),
        (1, u'Compiling'),
        (2, u'Judging'),
        (3, u'Completed'),
    )
    RESULT_CHOICES = (
        (0, u'None'),
        (1, u'Accepted'),
        # TODO
    )
    ERROR_CHOICES = (
        (0, u'None'),
        (1, u'Stack Overflow'),
        # TODO
    )
    problem = models.ForeignKey(Problem, related_name='submissions')
    user = models.ForeignKey(User, related_name='submissions')
    contest = models.ForeignKey(Contest, null=True, blank=True, default=None)
    language = models.ForeignKey(Language, related_name='+')
    code = models.TextField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    result = models.IntegerField(choices=RESULT_CHOICES, default=0)
    error = models.IntegerField(choices=ERROR_CHOICES, default=0)
    detail = models.TextField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    locked = models.BooleanField(default=False)
    judger = models.CharField(max_length=50)
    
class Settings(models.Model):
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

class UserProfile(models.Model):
    GENDER_CHOICES = (
        (u'M', u'Male'),
        (u'F', u'Female'),
    )
    
    user = models.ForeignKey(User, unique=True)
    realname = models.CharField(max_length=50)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    bio = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='profile/photo', null=True, blank=True)
    thumb_24 = models.ImageField(upload_to='profile/thumb24', null=True, blank=True, editable=False)
    thumb_48 = models.ImageField(upload_to='profile/thumb48', null=True, blank=True, editable=False)
    thumb_96 = models.ImageField(upload_to='profile/thumb96', null=True, blank=True, editable=False)
    starred_problems = models.ManyToManyField(Problem, related_name='+')
