# -*- coding: utf8 -*-
from django.db import models
from django.contrib import admin
from oj.models import *

admin.site.register(ProblemSet)
admin.site.register(Problem)
admin.site.register(ProblemAttribute)
admin.site.register(Comment)
admin.site.register(CommentAttachment)
admin.site.register(Team)
admin.site.register(Language)
admin.site.register(Contest)
admin.site.register(ContestUser)
admin.site.register(ContestTeam)
admin.site.register(Submission)
admin.site.register(Settings)
admin.site.register(UserProfile)
