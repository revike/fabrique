from datetime import datetime

from django.http import Http404
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from main_app.models import UserAnonymous, Answer, Survey
from django.contrib.sessions.models import Session


def key_session(request):
    key = request.session.session_key
    if key is None:
        request.session.create()
        key = request.session.session_key
    user_id = UserAnonymous.objects.filter(key=key).first()
    if not user_id:
        user_id = UserAnonymous.objects.create(key=key)
    request.session['user_id'] = user_id.id
    Session.objects.filter(session_key=key).first().expire_date = 99999999
    return user_id


def add_to_dict(request, answer_serial, question, kwargs):
    answer_dict = dict(answer_serial.validated_data)
    user_id = UserAnonymous.objects.get(
        id=request.session['user_id'])
    answer_dict['question_id'] = question.first()
    answer_dict['user_id'] = user_id
    answer_dict['survey_id'] = question.first().survey_id
    new_answer = Answer.objects.filter(
        question_id=kwargs['pk_id'],
        user_id=request.session['user_id']).update(**answer_dict)
    if not new_answer:
        Answer.objects.create(**answer_dict)


def get_list(self, kwargs):
    try:
        survey = Survey.objects.get(id=kwargs['pk'])
        if survey.finished_at <= datetime.now().date():
            survey.is_active = False
            survey.save()
        queryset = self.filter_queryset(
            self.get_queryset().filter(survey_id=survey.id))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    except AttributeError:
        raise Http404


def detail_object(self):
    survey = self.kwargs['pk']
    filter_kwargs = {self.lookup_field: self.kwargs['pk_id']}
    obj = get_object_or_404(
        self.queryset.filter(survey_id=survey),
        **filter_kwargs)
    self.check_object_permissions(self.request, obj)
    return obj
