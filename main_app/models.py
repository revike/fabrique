from django.db import models


class Survey(models.Model):
    """Survey table"""

    class Meta:
        verbose_name = 'опросы'
        verbose_name_plural = 'опросы'

    name = models.CharField(max_length=64, verbose_name='название опроса')
    description = models.TextField(blank=True, verbose_name='описание')
    created_at = models.DateField(auto_now_add=True, editable=False,
                                  verbose_name='дата и время создания')
    finished_at = models.DateField(verbose_name='дата окончания')
    is_active = models.BooleanField(default=True, db_index=True,
                                    verbose_name='активна')

    def __str__(self):
        return f'{self.name}'


class Question(models.Model):
    """Question table"""

    class Meta:
        verbose_name = 'вопросы'
        verbose_name_plural = 'вопросы'

    TEXT = 'TX'
    CHOICE = 'CH'
    MULTIPLE_CHOICE = 'MC'

    CHOICES_ANSWER = (
        (TEXT, 'текст'),
        (CHOICE, 'один вариант ответа'),
        (MULTIPLE_CHOICE, 'несколько вариантов ответа'),
    )

    survey_id = models.ForeignKey(to='Survey', on_delete=models.CASCADE,
                                  related_name='question',
                                  db_index=True, verbose_name='опрос')
    text = models.CharField(max_length=256, verbose_name='вопрос')
    answer_type = models.CharField(max_length=2, choices=CHOICES_ANSWER,
                                   verbose_name='тип ответа')
    is_active = models.BooleanField(default=True, db_index=True,
                                    verbose_name='активна')

    def __str__(self):
        return f'{self.text} - {self.answer_type}'


class OptionAnswer(models.Model):
    """Option for answer"""
    question_id = models.ForeignKey(to='Question', on_delete=models.CASCADE,
                                    related_name='option_answer',
                                    db_index=True, verbose_name='вопрос')
    option_answer_text = models.CharField(max_length=256,
                                          verbose_name='вариант ответа')

    def __str__(self):
        return f'{self.option_answer_text}'


class UserAnonymous(models.Model):
    """UserID table"""
    key = models.CharField(max_length=128, unique=True,
                           verbose_name='session_key')

    def __str__(self):
        return f'{self.id}'


class Answer(models.Model):
    """Answer table"""

    class Meta:
        verbose_name = 'ответы'
        verbose_name_plural = 'ответы'

    user_id = models.ForeignKey(to='UserAnonymous', on_delete=models.CASCADE,
                                related_name='answer', verbose_name='id user')
    survey_id = models.ForeignKey(to='Survey', on_delete=models.CASCADE,
                                  db_index=True, related_name='answer',
                                  verbose_name='опрос')
    question_id = models.ForeignKey(to='Question', on_delete=models.CASCADE,
                                    related_name='answer',
                                    db_index=True, verbose_name='вопрос')
    option_answer_text = models.ManyToManyField(
        to='OptionAnswer',
        related_name='answer',
        verbose_name='опциональный ответ')
    answer_text = models.CharField(max_length=256, verbose_name='ответ')
    created_at = models.DateField(auto_now_add=True,
                                  verbose_name='дата и время ответа')

    def __str__(self):
        return f'{self.question_id.text} - {self.answer_text}'
