from django.contrib import admin

from main_app.models import Survey, Question, Answer

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Answer)
