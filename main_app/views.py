from datetime import datetime

from django.contrib.sessions.models import Session
from django.http import Http404
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response

from main_app.models import Survey, Question, OptionAnswer, Answer, \
    UserAnonymous
from main_app.serializers import SurveyModelSerializer, \
    QuestionModelSerializer, OptionAnswerModelSerializer, AnswerModelSerializer


class AdminSurveyList(generics.ListAPIView, generics.CreateAPIView):
    """APIView for Survey Admin"""
    queryset = Survey.objects.filter(is_active=True)
    serializer_class = SurveyModelSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        finish = serializer.validated_data['finished_at']
        if finish <= datetime.now().date():
            raise Exception('Invalid Date Finish')
        return super().create(self.request)

    def list(self, request, *args, **kwargs):
        for survey in self.get_queryset().filter(is_active=True):
            if survey.finished_at <= datetime.now().date():
                survey.is_active = False
                survey.save()
        return super().list(self.request)


class AdminSurveyDetail(generics.RetrieveAPIView,
                        generics.UpdateAPIView,
                        generics.DestroyAPIView):
    """APIView for Survey Detail Admin"""
    serializer_class = SurveyModelSerializer
    queryset = Survey.objects.filter(is_active=True)
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        finish = serializer.validated_data['finished_at']
        if finish <= datetime.now().date():
            raise Exception('Invalid Date Finish')
        return super().update(self.request)

    def retrieve(self, request, *args, **kwargs):
        survey = self.queryset.filter(id=self.get_object().id)
        if survey.first().finished_at <= datetime.now().date():
            survey.first().is_active = False
            survey.first().save()
            raise Exception('Survey Finished')
        return super().retrieve(self.request)


class AdminQuestionList(generics.ListAPIView, generics.CreateAPIView):
    """APIView for Question Admin"""
    queryset = Question.objects.filter(is_active=True,
                                       survey_id__is_active=True)
    serializer_class = QuestionModelSerializer
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        try:
            survey = Survey.objects.get(id=kwargs['pk'])
            if survey.finished_at <= datetime.now().date():
                survey.is_active = False
                survey.save()
            queryset = self.filter_queryset(
                self.get_queryset().filter(survey_id=survey.id,
                                           survey_id__is_active=True))
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except AttributeError:
            raise Http404

    def create(self, request, *args, **kwargs):
        survey = Survey.objects.get(id=kwargs['pk'])
        quest_serial = QuestionModelSerializer(data=request.data)
        quest_serial.is_valid(raise_exception=True)
        quest_dict = dict(quest_serial.validated_data)
        quest_dict['survey_id'] = survey
        new_quest = Question(**quest_dict)
        new_quest.save()
        result = QuestionModelSerializer(new_quest)
        headers = self.get_success_headers(result.data)
        return Response(result.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class AdminQuestionDetail(generics.RetrieveAPIView,
                          generics.UpdateAPIView,
                          generics.DestroyAPIView):
    """APIView for Question Detail Admin"""
    queryset = Question.objects.filter(is_active=True,
                                       survey_id__is_active=True)
    serializer_class = QuestionModelSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        survey = self.kwargs['pk']
        filter_kwargs = {self.lookup_field: self.kwargs['pk_id']}
        obj = get_object_or_404(
            self.queryset.filter(survey_id=survey, survey_id__is_active=True),
            **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self, request, *args, **kwargs):
        survey = Survey.objects.filter(id=kwargs['pk'])
        if survey.first().finished_at <= datetime.now().date():
            survey.first().is_active = False
            survey.first().save()
            raise Exception('Survey Finished')
        return super().retrieve(self.request)


class AdminOptionAnswerList(generics.ListAPIView, generics.CreateAPIView):
    """APIView for OptionAnswer Admin"""
    queryset = OptionAnswer.objects.filter(
        question_id__survey_id__is_active=True)
    serializer_class = OptionAnswerModelSerializer
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        try:
            survey = Survey.objects.get(id=kwargs['pk'])
            if survey.finished_at <= datetime.now().date():
                survey.is_active = False
                survey.save()
            answer_types = ['CH', 'MC']
            question_id = kwargs['pk_id']
            answer = Question.objects.filter(id=question_id)
            answer_type = answer.first().answer_type
            if answer_type in answer_types:
                survey = Survey.objects.get(id=kwargs['pk'])
                question = Question.objects.get(id=kwargs['pk_id'])
                queryset = self.filter_queryset(
                    self.get_queryset().filter(
                        question_id=question.id,
                        question_id__survey_id=survey,
                        question_id__survey_id__is_active=True))
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response(serializer.data)

                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
            raise Http404
        except AttributeError:
            raise Http404

    def create(self, request, *args, **kwargs):
        answer_types = ['CH', 'MC']
        question_id = kwargs['pk_id']
        question = Question.objects.get(id=question_id)
        answer_type = question.answer_type
        if answer_type in answer_types:
            option_serial = OptionAnswerModelSerializer(data=request.data)
            option_serial.is_valid(raise_exception=True)
            option_dict = dict(option_serial.validated_data)
            option_dict['question_id'] = question
            new_option = OptionAnswer(**option_dict)
            new_option.save()
            result = OptionAnswerModelSerializer(new_option)
            headers = self.get_success_headers(result.data)
            return Response(result.data, status=status.HTTP_201_CREATED,
                            headers=headers)
        raise Exception('Not Text answer')


class AdminOptionAnswerDetail(generics.RetrieveAPIView,
                              generics.UpdateAPIView,
                              generics.DestroyAPIView):
    """APIView for OptionAnswer Admin"""
    queryset = OptionAnswer.objects.filter(
        question_id__survey_id__is_active=True)
    serializer_class = OptionAnswerModelSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        question = self.kwargs['pk_id']
        filter_kwargs = {self.lookup_field: self.kwargs['id']}
        obj = get_object_or_404(self.queryset.filter(question_id=question),
                                **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self, request, *args, **kwargs):
        survey = Survey.objects.filter(id=kwargs['pk'])
        if survey.first().finished_at <= datetime.now().date():
            survey.first().is_active = False
            survey.first().save()
            raise Exception('Survey Finished')
        return super().retrieve(self.request)


class SurveyList(generics.ListAPIView):
    """APIView for Survey"""
    queryset = Survey.objects.filter(is_active=True)
    serializer_class = SurveyModelSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        for survey in self.get_queryset().filter(is_active=True):
            if survey.finished_at <= datetime.now().date():
                survey.is_active = False
                survey.save()
        return super().list(self.request)


class SurveyDetail(generics.RetrieveAPIView):
    """APIView for Survey"""
    queryset = Survey.objects.filter(is_active=True)
    serializer_class = SurveyModelSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        survey = Survey.objects.filter(id=kwargs['pk'])
        if survey.first().finished_at <= datetime.now().date():
            survey.first().is_active = False
            survey.first().save()
            raise Exception('Survey Finished')
        return super().retrieve(self.request)


class QuestionList(generics.ListAPIView):
    """APIView for Survey"""
    queryset = Question.objects.filter(survey_id__is_active=True)
    serializer_class = QuestionModelSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        return AdminQuestionList.list(self=self, request=request, *args,
                                      **kwargs)


class QuestionDetail(generics.RetrieveAPIView):
    """APIView for Survey"""
    queryset = Question.objects.filter(survey_id__is_active=True)
    serializer_class = QuestionModelSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return AdminQuestionDetail.get_object(self)


class AnswerView(generics.ListAPIView, generics.CreateAPIView): # Error
    """APIView for Answer"""
    queryset = Answer.objects.filter(survey_id__is_active=True)
    serializer_class = AnswerModelSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        survey = self.kwargs['pk']
        question = self.kwargs['pk_id']
        filter_kwargs = {self.lookup_field: self.kwargs['pk_id']}
        obj = get_object_or_404(
            self.queryset.filter(question_id=question, survey_id=survey),
            **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def list(self, request, *args, **kwargs):
        key = request.session.session_key
        if key is None:
            request.session.create()
            key = request.session.session_key
        user_id = UserAnonymous.objects.filter(key=key).first()
        if not user_id:
            user_id = UserAnonymous.objects.create(key=key)
        self.request.session['user_id'] = user_id.id
        Session.objects.filter(session_key=key).first().expire_date = 99999999

        return super().list(self.request)

    def create(self, request, *args, **kwargs):
        types = ['CH', 'MC']
        question = Question.objects.filter(id=kwargs['pk_id'],
                                           survey_id=kwargs['pk'])
        type_answer = question.first().answer_type
        if type_answer in types:
            answer_serial = AnswerModelSerializer(data=request.data)
            answer_serial.is_valid(raise_exception=True)
            answer_dict = dict(answer_serial.validated_data)
            user_id = UserAnonymous.objects.get(
                id=self.request.session['user_id'])
            answer_dict['answer_text'] = ''
            answer_dict['question_id'] = question.first()
            answer_dict['user_id'] = user_id
            answer_dict['survey_id'] = question.first().survey_id
            new_answer = Answer(**answer_dict) # Error
            new_answer.save()
            result = AnswerModelSerializer()
            headers = self.get_success_headers(result.data)
            return Response(result.data, status=status.HTTP_201_CREATED,
                            headers=headers)
        else:
            return super().create(self.request)
