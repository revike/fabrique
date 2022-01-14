"""fabrique URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .documentations import urlpatterns as urls
from main_app import views as main

urlpatterns = [
    path('admin-api/', include([
        path('survey/', main.AdminSurveyList.as_view()),
        path('survey/<int:pk>/', main.AdminSurveyDetail.as_view()),
        path('survey/<int:pk>/question/', main.AdminQuestionList.as_view()),
        path('survey/<int:pk>/question/<int:pk_id>/',
             main.AdminQuestionDetail.as_view()),
        path('survey/<int:pk>/question/<int:pk_id>/option-answer/',
             main.AdminOptionAnswerList.as_view()),
        path('survey/<int:pk>/question/<int:pk_id>/option-answer/<int:id>/',
             main.AdminOptionAnswerDetail.as_view()),
    ])),
    path('survey/', main.SurveyList.as_view()),
    path('survey/<int:pk>/', main.SurveyDetail.as_view()),
    path('survey/<int:pk>/question/', main.QuestionList.as_view()),
    path('survey/<int:pk>/question/<int:pk_id>/',
         main.QuestionDetail.as_view()),
    path('survey/<int:pk>/question/<int:pk_id>/answer/',
         main.AnswerView.as_view()),
    path('answers/', main.AnswerUserList.as_view()),

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns += urls

urlpatterns = format_suffix_patterns(urlpatterns)
