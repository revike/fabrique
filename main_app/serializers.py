from rest_framework.serializers import ModelSerializer

from main_app.models import Survey, Question, OptionAnswer, Answer


class AnswerModelSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class OptionAnswerModelSerializer(ModelSerializer):
    class Meta:
        model = OptionAnswer
        fields = ('id', 'question_id', 'option_answer_text')


class QuestionModelSerializer(ModelSerializer):
    option_answer = OptionAnswerModelSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = (
            'id', 'survey_id', 'text', 'answer_type', 'option_answer')


class SurveyModelSerializer(ModelSerializer):
    question = QuestionModelSerializer(many=True, read_only=True)
    answer = AnswerModelSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = (
            'id', 'name', 'description', 'created_at', 'finished_at',
            'question', 'answer')
