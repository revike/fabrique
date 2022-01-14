from rest_framework.serializers import ModelSerializer
from main_app.models import Survey, Question, OptionAnswer, Answer


class AnswerAdminSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class AnswerModelSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = ('option_answer_text',)


class AnswerTextModelSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = ('answer_text',)


class OptionAnswerModelSerializer(ModelSerializer):
    class Meta:
        model = OptionAnswer
        fields = ('id', 'option_answer_text')


class QuestionModelSerializer(ModelSerializer):
    option_answer = OptionAnswerModelSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = (
            'id', 'text', 'answer_type', 'option_answer')


class SurveyModelSerializer(ModelSerializer):
    question = QuestionModelSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = (
            'id', 'name', 'description', 'created_at', 'finished_at',
            'question', 'is_active')


class SurveyAdminModelSerializer(ModelSerializer):
    question = QuestionModelSerializer(many=True, read_only=True)
    answer = AnswerAdminSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = (
            'id', 'name', 'description', 'created_at', 'finished_at',
            'question', 'answer', 'is_active')
